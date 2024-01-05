import numpy as np
from PIL import Image

laplace_core1 = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
laplace_core2 = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])


def set_window_size(root):
    # Set the window to the middle of the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (800 / 2))
    y = int((screen_height / 2) - (600 / 2))
    root.geometry(f"800x600+{x}+{y}")


def resize_image(image, size, x, y):
    l, h = size
    r1 = x / 2.5 / l
    r2 = y / 1.5 / h
    r = min(r1, r2)

    # Calculate the new width and height based on the ratio
    new_width = int(l * r)
    new_height = int(h * r)

    # Resize the image
    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

    return resized_image
