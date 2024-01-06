import numpy as np
from PIL import Image

def inv_degradation_function(shape, k):
    rows, cols = shape
    u = np.fft.fftfreq(rows)
    v = np.fft.fftfreq(cols)
    u, v = np.meshgrid(u, v)
    h_uv = np.exp(-k * (u**2 + v**2)**(5/6))
    return h_uv

def wiener_filter_calc(shape, k, gamma):
    rows, cols = shape
    u = np.fft.fftfreq(rows)
    v = np.fft.fftfreq(cols)
    u, v = np.meshgrid(u, v)
    h_uv = np.exp(-k * (u**2 + v**2)**(5/6))
    w_uv = np.conj(h_uv) / (np.abs(h_uv)**2 + gamma)
    return w_uv

def inverse_filter(image, k):
    # Convert the image to a numpy array
    image_array = np.array(image, dtype=np.float32)

    # Get the dimensions of the image
    height, width, channels = image_array.shape

    # Perform the Fourier transform for each color channel
    image_fft = np.fft.fft2(image_array, axes=(0, 1))
    image_fft_shifted = np.fft.fftshift(image_fft, axes=(0, 1))

    # Calculate the inverse degradation function
    h_uv = inv_degradation_function((height, width), k)

    # Apply the inverse filter independently to each color channel
    f_uv = np.zeros_like(image_fft_shifted, dtype=np.complex64)
    for c in range(channels):
        f_uv[:, :, c] = np.divide(image_fft_shifted[:, :, c], h_uv.T)

    # Perform the inverse Fourier transform
    filtered_image_array = np.abs(np.fft.ifft2(f_uv, axes=(0, 1)))

    # Clip the values to the valid range [0, 255]
    filtered_image_array = np.clip(filtered_image_array, 0, 255)

    # Convert the filtered image back to unsigned 8-bit integers
    filtered_image = filtered_image_array.astype(np.uint8)

    # Convert the filtered image back to a PIL image
    filtered_image = Image.fromarray(filtered_image)

    return filtered_image

def wiener_filter(image, k, gamma):
    # Convert the image to a numpy array
    image_array = np.array(image, dtype=np.float32)

    # Get the dimensions of the image
    height, width, channels = image_array.shape

    # Perform the Fourier transform for each color channel
    image_fft = np.fft.fft2(image_array, axes=(0, 1))
    image_fft_shifted = np.fft.fftshift(image_fft, axes=(0, 1))

    # Calculate the Wiener filter
    w_uv = wiener_filter_calc((height, width), k, gamma)

    # Apply the Wiener filter independently to each color channel
    f_wiener_uv = np.zeros_like(image_fft_shifted, dtype=np.complex64)
    for c in range(channels):
        f_wiener_uv[:, :, c] = np.multiply(image_fft_shifted[:, :, c], w_uv.T)

    # Perform the inverse Fourier transform
    restored_image_wiener_array = np.abs(np.fft.ifft2(f_wiener_uv, axes=(0, 1)))

    # Clip the values to the valid range [0, 255]
    restored_image_wiener_array = np.clip(restored_image_wiener_array, 0, 255)

    # Convert the restored image back to unsigned 8-bit integers
    restored_image_wiener = restored_image_wiener_array.astype(np.uint8)

    # Convert the restored image back to a PIL image
    restored_image_wiener = Image.fromarray(restored_image_wiener)

    return restored_image_wiener
