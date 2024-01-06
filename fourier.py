from PIL import Image
import numpy as np
from scipy import signal
from scipy.ndimage import gaussian_filter


def fourier_transform(image):
    """
    :param image: PIL image
    :return: the Fourier transform of the image, displayed in the Fourier domain
    """
    # convert the image to numpy array
    image = np.array(image, dtype=np.int32)

    # perform the Fourier transform
    image_fft = np.fft.fft2(image)

    # shift the zero-frequency component to the center of the spectrum
    image_fft = np.fft.fftshift(image_fft)

    # calculate the magnitude of the Fourier transform
    magnitude_spectrum = np.abs(image_fft)

    # convert the magnitude spectrum to the range of [0, 255]
    magnitude_spectrum = magnitude_spectrum / magnitude_spectrum.max() * 255

    # convert the magnitude spectrum to uint8
    magnitude_spectrum = magnitude_spectrum.astype(np.uint8)

    # convert the magnitude spectrum back to PIL image
    magnitude_spectrum = Image.fromarray(magnitude_spectrum)

    return magnitude_spectrum

def gaussian_low_pass_filter(image, sigma):
    """
    :param image: RGB PIL image
    """
    # convert the image to numpy array
    image = np.array(image, dtype=np.int32)

    # apply Gaussian low-pass filter
    filtered_image = gaussian_filter(image, sigma=sigma)

    # clip the values to the valid range [0, 255]
    filtered_image = np.clip(filtered_image, 0, 255)

    # convert the filtered image to unsigned 8-bit integers
    filtered_image = filtered_image.astype(np.uint8)

    # convert the filtered image back to PIL image
    filtered_image = Image.fromarray(filtered_image)

    return filtered_image

def gaussian_high_pass_filter(image, sigma):
    """
    :param image: RGB PIL image
    """
    # convert the image to numpy array
    image = np.array(image, dtype=np.int32)

    # apply Gaussian low-pass filter
    filtered_image = gaussian_filter(image, sigma=sigma)

    filtered_image = image - filtered_image

    # clip the values to the valid range [0, 255]
    filtered_image = np.clip(filtered_image, 0, 255)

    # convert the filtered image to unsigned 8-bit integers
    filtered_image = filtered_image.astype(np.uint8)

    # convert the filtered image back to PIL image
    filtered_image = Image.fromarray(filtered_image)

    return filtered_image


import numpy as np
from scipy import signal
from PIL import Image

def butterworth_low_pass_filter(image, cutoff_frequency, order):
    """
    :param image: RGB PIL image
    """
    # Convert the image to a numpy array
    image_array = np.array(image, dtype=np.float32)

    # Get the dimensions of the image
    height, width, channels = image_array.shape

    # Perform the Fourier transform for each color channel
    image_fft = np.fft.fft2(image_array, axes=(0, 1))

    # Create a Butterworth low-pass filter
    rows, cols = height, width
    mask = np.ones((rows, cols))

    # Apply the filter independently to each color channel
    for c in range(channels):
        c_mask = mask - signal.butter(order, cutoff_frequency, output='sos', analog=False, fs=1)[..., 0]

        # Apply the filter to the image in the frequency domain for the current channel
        filtered_image_fft = image_fft[:, :, c] * c_mask

        # Convert the filtered image back to the spatial domain for the current channel
        filtered_image_channel = np.fft.ifft2(filtered_image_fft).real

        # Clip the values to the valid range [0, 255] for the current channel
        filtered_image_channel = np.clip(filtered_image_channel, 0, 255)

        # Update the channel in the original image array
        image_array[:, :, c] = filtered_image_channel

    # Convert the filtered image back to unsigned 8-bit integers
    filtered_image_array = image_array.astype(np.uint8)

    # Convert the filtered image back to a PIL image
    filtered_image = Image.fromarray(filtered_image_array)

    return filtered_image


def butterworth_high_pass_filter(image, cutoff_frequency, order):
    """
    :param image: RGB PIL image
    """
    # Convert the image to a numpy array
    image_array = np.array(image, dtype=np.float32)

    # Get the dimensions of the image
    height, width, channels = image_array.shape

    # Perform the Fourier transform for each color channel
    image_fft = np.fft.fft2(image_array, axes=(0, 1))

    # Create a Butterworth high-pass filter
    rows, cols = height, width
    mask = np.ones((rows, cols))

    # Apply the filter independently to each color channel
    for c in range(channels):
        c_mask = mask - signal.butter(order, cutoff_frequency, btype='high', output='sos', analog=False, fs=1)[..., 0]

        # Apply the filter to the image in the frequency domain for the current channel
        filtered_image_fft = image_fft[:, :, c] * c_mask

        # Convert the filtered image back to the spatial domain for the current channel
        filtered_image_channel = np.fft.ifft2(filtered_image_fft).real

        # Clip the values to the valid range [0, 255] for the current channel
        filtered_image_channel = np.clip(filtered_image_channel, 0, 255)

        # Update the channel in the original image array
        image_array[:, :, c] = filtered_image_channel

    # Convert the filtered image back to unsigned 8-bit integers
    filtered_image_array = image_array.astype(np.uint8)

    # Convert the filtered image back to a PIL image
    filtered_image = Image.fromarray(filtered_image_array)

    return filtered_image