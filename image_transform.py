import sys

import numpy as np
from PIL import Image
from scipy.ndimage import convolve
from scipy.ndimage import uniform_filter as uniform_filter_scipy, median_filter as median_filter_scipy

def clip(image):
    """
    clip the image to 0-255
    """
    return np.clip(image, 0, 255).astype(np.uint8)


def greyscale_transform(image):
    """
    transform image to greyscale
    :param image: PIL image
    :return: greyscale image
    """
    image = image.convert("L")
    return image


def power_law_image(image, gamma, c):
    """
    :param image: PIL image
    """
    # if the image is not in greyscale, convert it to greyscale
    if image.mode != "L":
        image = greyscale_transform(image)

    # convert the image to numpy array
    image = np.array(image, dtype=np.int32)

    image = np.power(image / 255.0, gamma) * 255.0 * c
    image = image.astype(np.uint8)
    image = clip(image)

    # convert the image back to PIL image
    image = Image.fromarray(image)

    return image


def gamma_correction(image, gamma, c):
    # convert the image to numpy array
    image = np.array(image, dtype=np.int32)

    image = np.power(image / c, gamma) * c
    image = image.astype(np.uint8)
    image = clip(image)

    # convert the image back to PIL image
    image = Image.fromarray(image)

    return image


def mean_filter(image, kernel_size):
    """
    filter the RGB image with mean filter
    :param image: PIL image
    :param kernel_size: int
    """
    # convert the image to numpy array
    image = np.array(image, dtype=np.int32)

    # filter the image
    filtered_image = uniform_filter_scipy(image, size=(kernel_size, kernel_size, 1))

    # clip the values to the valid range [0, 255]
    filtered_image = clip(filtered_image)

    # convert the image back to PIL image
    filtered_image = Image.fromarray(filtered_image)

    return filtered_image


def median_filter(image, kernel_size):
    """
    filter the RGB image with median filter
    :param image: PIL image
    :param kernel_size: int
    """
    # convert the image to numpy array
    image = np.array(image, dtype=np.int32)

    # filter the image
    filtered_image = median_filter_scipy(image, size=(kernel_size, kernel_size, 1))

    # clip the values to the valid range [0, 255]
    filtered_image = clip(filtered_image)

    # convert the image back to PIL image
    filtered_image = Image.fromarray(filtered_image)

    return filtered_image


def invert(image):
    """
    invert the image
    :param image: PIL image
    """
    # convert the image to numpy array
    image = np.array(image, dtype=np.int32)

    image = 255 - image
    image = image.astype(np.uint8)

    # convert the image back to PIL image
    image = Image.fromarray(image)

    return image


def laplace_filter(image, core):
    """
    :param image: PIL image
    :param core: core1 or core2
    :return: filtered image
    """
    # convert the image to numpy array
    image = np.array(image, dtype=np.int32)

    # size of the image
    height, width, channels = image.shape

    # create a new image with the same size as the original image
    filtered_image = np.zeros((height, width, channels), dtype=np.int32)

    # radius of the kernel
    radius = len(core) // 2

    # Convolve the image with the Laplace filter kernel
    for c in range(channels):
        filtered_image[:, :, c] = convolve(image[:, :, c], core, mode='constant')

    # clip the values to the valid range [0, 255]
    filtered_image = clip(filtered_image)
    filtered_image = filtered_image.astype(np.uint8)

    # convert the image back to PIL image
    filtered_image = Image.fromarray(filtered_image)

    return filtered_image
