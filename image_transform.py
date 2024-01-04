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
    幂律变换
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
    """
    伽马校正
    """
    # convert the image to numpy array
    image = np.array(image, dtype=np.int32)

    image = np.power(image / c, gamma) * c
    image = image.astype(np.uint8)
    image = clip(image)

    # convert the image back to PIL image
    image = Image.fromarray(image)

    return image