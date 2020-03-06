from typing import List, Any
import struct
from osgeo import gdal
import numpy as np

print("Version: {}".format(gdal.__version__))

dataset: gdal.Dataset = gdal.Open("L3-NE43H01-094-059-04Apr15-BAND2.tif", gdal.GA_ReadOnly)
if not dataset:
    print("File nahiye")
    exit()

print("\nDriver: {0}/{1}".format(dataset.GetDriver().ShortName, dataset.GetDriver().LongName))
print("Size: {} X {} X {}".format(dataset.RasterXSize, dataset.RasterYSize, dataset.RasterCount))
print("Projection is {}".format(dataset.GetProjection()))
geotransform = dataset.GetGeoTransform()
print("Origin = ({}, {})".format(geotransform[0], geotransform[3]))
print("Pixel Size = ({}, {})".format(geotransform[1], geotransform[5]))
print("Rotation = ({}, {})".format(geotransform[2], geotransform[4]))

bands: List[gdal.Band] = [dataset.GetRasterBand(1)]

print("\nBand type: {}\n".format(gdal.GetDataTypeName(bands[0].DataType)))

for band in bands:
    min = band.GetMinimum()
    max = band.GetMaximum()
    if not min or not max:
        min, max = band.ComputeRasterMinMax(True)
    print("Min={:.3f}, Max={:.3f}".format(min, max))
    if band.GetOverviewCount() > 0:
        print("Band has {} overviews".format(band.GetOverviewCount()))
    if band.GetRasterColorTable():
        print("Band has a color table with {} entries".format(band.GetRasterColorTable().GetCount()))
    # print("XSize, Ysize : {}, {}".format(band.XSize, band.YSize))
    scanline = band.ReadRaster(xoff=0, yoff=0,
                               xsize=band.XSize, ysize=1,
                               buf_xsize=band.XSize, buf_ysize=1,
                               buf_type=gdal.GDT_Float32)
    tuple_of_floats = struct.unpack("f"*band.XSize, scanline)

driver: gdal.Driver = dataset.GetDriver()
new_dataset: gdal.Dataset = driver.CreateCopy("ndvi_band.tif", dataset, strict=0)

nir_band = bands[0]
green_band = bands[1]
red_band = bands[2]

nir_array = nir_band.ReadAsArray()
green_array = green_band.ReadAsArray()
red_array = red_band.ReadAsArray()
ndvi_array = ((nir_array-red_array)/(nir_array+red_array)+1)*511.5

raster = np.array([[0 for c in range(nir_band.XSize)] for r in range(nir_band.YSize)])

new_dataset.GetRasterBand(1).WriteArray(ndvi_array)
# Set all values in Red and Green band to 0
# new_dataset.GetRasterBand(2).WriteArray(raster)
# new_dataset.GetRasterBand(3).WriteArray(raster)

dataset = None
new_dataset = None
