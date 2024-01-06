import sys

import numpy as np
from PIL import Image


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

    # get the height and width of the image
    height, width = image.shape[:2]

    # create a new image with the same size as the original image
    filtered_image = np.zeros((height, width), dtype=np.uint8)

    # calculate the radius of the kernel
    radius = kernel_size // 2

    # filter the image
    for i in range(height):
        for j in range(width):
            # get the neighbors of the current pixel
            neighbors = []
            for k in range(-radius, radius + 1):
                for l in range(-radius, radius + 1):
                    # check if the neighbor is out of bound
                    if i + k >= 0 and i + k < height and j + l >= 0 and j + l < width:
                        neighbors.append(image[i + k, j + l])

            # calculate the mean value of the neighbors and assign it to the current pixel
            python_version = sys.version_info.major
            python_version_minor = sys.version_info.minor
            if python_version == 3 and python_version_minor <= 9:
                mean_value = sum(sum(neighbors) // len(neighbors[0]))
            else:
                mean_value = sum(neighbors) // len(neighbors)
            filtered_image[i, j] = mean_value

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

    # get the height and width of the image
    height, width = image.shape[:2]

    # create a new image with the same size as the original image
    filtered_image = np.zeros((height, width), dtype=np.uint8)

    # calculate the radius of the kernel
    radius = kernel_size // 2

    # filter the image
    for i in range(height):
        for j in range(width):
            # get the neighbors of the current pixel
            neighbors = []
            for k in range(-radius, radius + 1):
                for l in range(-radius, radius + 1):
                    # check if the neighbor is out of bound
                    if i + k >= 0 and i + k < height and j + l >= 0 and j + l < width:
                        neighbors.append(image[i + k, j + l])

            # sort the neighbors and assign the median value to the current pixel
            neighbors.sort()
            filtered_image[i, j] = neighbors[len(neighbors) // 2]

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


def laplace_filter(image, kernel):
    """
    filter the image with laplace filter
    :param image: PIL image
    :param kernel: numpy array
    """
    # convert the image to numpy array
    image = np.array(image, dtype=np.int32)

    image = np.convolve(image, kernel, mode="same")
    image = image.astype(np.uint8)

    # convert the image back to PIL image
    image = Image.fromarray(image)

    return image
