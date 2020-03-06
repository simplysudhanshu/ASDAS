from osgeo import gdal
import numpy as np
import cv2


def format_save(save_name, x_size, y_size, r_array, g_array, b_array):
    r_array_form = r_array.astype(dtype='uint8')
    g_array_form = g_array.astype(dtype='uint8')
    b_array_form = b_array.astype(dtype='uint8')
    # print("Formed")
    new_image = np.array([
        [b_array_form[r, c], g_array_form[r, c], r_array_form[r, c]]
        for r in range(y_size) for c in range(x_size)])
    # print("Array created")
    new_image = new_image.astype(dtype='uint8')
    new_image = new_image.reshape((y_size, x_size, 3))
    factor = min(1600 / x_size, 600 / y_size)
    new_image = cv2.resize(new_image, dsize=(0, 0), fx=factor, fy=factor)
    cv2.imwrite(save_name, new_image)


def create_original(image_name):
    dataset: gdal.Dataset = gdal.Open(image_name, gdal.GA_ReadOnly)
    x_size = dataset.RasterXSize
    y_size = dataset.RasterYSize
    r_array = dataset.GetRasterBand(3).ReadAsArray()
    g_array = dataset.GetRasterBand(2).ReadAsArray()
    b_array = dataset.GetRasterBand(1).ReadAsArray()
    format_save("original_"+image_name[:-3]+"png", x_size, y_size, r_array, g_array, b_array)


def transform_image(image_nameR, image_nameG, image_nameB, r_text, g_text, b_text, gray=None, save=False, save_name=None):
    datasetR: gdal.Dataset = gdal.Open(image_nameR, gdal.GA_ReadOnly)
    datasetG: gdal.Dataset = gdal.Open(image_nameG, gdal.GA_ReadOnly)
    datasetB: gdal.Dataset = gdal.Open(image_nameB, gdal.GA_ReadOnly)

    x_size = datasetR.RasterXSize
    y_size = datasetR.RasterYSize

    r_array = datasetR.GetRasterBand(1).ReadAsArray()
    g_array = datasetG.GetRasterBand(1).ReadAsArray()
    b_array = datasetB.GetRasterBand(1).ReadAsArray()

    # ---------------------------------------------------

    R = r_array
    G = g_array
    NIR = b_array
    NDVI = ((NIR - R)/(NIR + R)+1)*511.5

    # ---------------------------------------------------

    evals_rgb = [eval(r_text), eval(g_text), eval(b_text)]
    values_rgb = []
    for val in evals_rgb:
        if isinstance(val, int):
            values_rgb.append(np.array([[val for c in range(x_size)] for r in range(y_size)]))
        else:
            values_rgb.append(val)
    if save:
        driver: gdal.Driver = datasetR.GetDriver()
        new_dataset: gdal.Dataset = driver.CreateCopy(save_name, datasetR, strict=0)
        new_dataset.GetRasterBand(3).WriteArray(values_rgb[0])
        new_dataset.GetRasterBand(2).WriteArray(values_rgb[1])
        new_dataset.GetRasterBand(1).WriteArray(values_rgb[2])
    else:
        format_save("preview_"+image_nameR[:-3]+"png", x_size, y_size, *values_rgb)
