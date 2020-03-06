import numpy as np
import cv2


def find_min(x, y):
    if x <= y:
        return x
    else:
        return y


def negate(old):
    return -old


def z(old):
    return (old - min) * 255 / (max - min)


def format_save(save_name, x_size, y_size, r_array, g_array, b_array):
    r_array_form = r_array.astype(dtype='uint8')
    g_array_form = g_array.astype(dtype='uint8')
    b_array_form = b_array.astype(dtype='uint8')

    new_image = np.array([
        [b_array_form[r, c], g_array_form[r, c], r_array_form[r, c]]
        for r in range(y_size) for c in range(x_size)])

    print("Array created")

    new_image = new_image.astype(dtype='uint8')
    new_image = new_image.reshape((y_size, x_size, 3))
    factor = find_min(1600 / x_size, 600 / y_size)
    new_image = cv2.resize(new_image, dsize=(0, 0), fx=factor, fy=factor)
    cv2.imwrite(save_name, new_image)

    print("IMAGE FORMED !")


dataframe = np.genfromtxt('ndvi.csv', delimiter=',')
x, y = dataframe.shape

negate_dataframe = np.array(negate(dataframe))

min = negate_dataframe.min()
max = negate_dataframe.max()

dataframe_new = np.array(z(negate_dataframe))


values_rgb = [np.array([[0 for c in range(x)] for r in range(y)]), dataframe_new,
              np.array([[0 for c in range(x)] for r in range(y)])]

format_save(save_name="NDVI_image.png", x_size=x, y_size=y,
            r_array=values_rgb[0], g_array=values_rgb[1], b_array=values_rgb[2])
