import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter
from image_transform import *
from support import *
from equalizeHist import *
from addnoise import *
from functools import partial


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")

        set_window_size(root)

        # Variables
        self.image_list = []
        self.current_index = 0
        self.current_directory = ""

        # UI Elements
        self.canvas = tk.Canvas(root)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # Menu Bar
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Exit", command=root.destroy)

        # Image Processing Options
        process_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Process", menu=process_menu)
        process_menu.add_command(label="Default", command=self.default)
        process_menu.add_command(label="Blur", command=self.blur_image)
        process_menu.add_command(label="Exponential grayscale transformation", command=self.exp_grayscale)
        process_menu.add_command(label="Gamma correction", command=self.gamma_correction)
        process_menu.add_command(label="Mean filter", command=self.mean_filter)
        # process_menu.add_command(label="Median filter", command=self.median_filter)
        # process_menu.add_command(label="Invert", command=self.invert)
        # process_menu.add_command(label="Laplace filter", command=self.laplace_filter)
        process_menu.add_command(label="Histogram equalization", command=self.hist_qualization)

        # Add noise Options
        Noise_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Add noise", menu=Noise_menu)
        Noise_menu.add_command(label="Default", command=self.default)
        Noise_menu.add_command(label="Gaussian", command=partial(self.Add_noise, "Gaussian"))
        Noise_menu.add_command(label="Salt Pepper", command=partial(self.Add_noise, "Salt Pepper"))
        Noise_menu.add_command(label="Gamma", command=partial(self.Add_noise, "Gamma"))
        Noise_menu.add_command(label="Uniform", command=partial(self.Add_noise, "Uniform"))
        Noise_menu.add_command(label="Exponential", command=partial(self.Add_noise, "Exponential"))
        Noise_menu.add_command(label="Rayleigh", command=partial(self.Add_noise, "Rayleigh"))

        # Navigation Buttons
        self.nav_frame = tk.Frame(root)
        self.nav_frame.pack(side=tk.BOTTOM, pady=10)
        self.prev_button = tk.Button(self.nav_frame, text="Previous", command=self.show_previous_image)
        self.prev_button.pack(side=tk.LEFT, padx=20, ipadx=10)
        self.next_button = tk.Button(self.nav_frame, text="Next", command=self.show_next_image)
        self.next_button.pack(side=tk.LEFT, padx=20, ipadx=10)
        self.save_button = tk.Button(self.nav_frame, text="Save processed image", command=self.save_image)
        self.save_button.pack(side=tk.LEFT, padx=20)

        self.processed_image = None
        self.original_image = None
        self.image_size = None
        self.using_transformations = None

    def open_image(self):
        self.current_directory = filedialog.askdirectory()
        if self.current_directory:
            self.image_list = [f for f in os.listdir(self.current_directory) if
                               f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
            if not self.image_list:
                tk.messagebox.showinfo("Error", "The directory {} does not contain any images, please check you "
                                                "directory.".format(self.current_directory))
                self.current_directory = ""
                return
            if self.image_list:
                self.current_index = 0
                self.load_current_image()

    def load_current_image(self):
        if self.image_list:
            image_path = os.path.join(self.current_directory, self.image_list[self.current_index])
            # test if the directory is valid and the file is an image
            if not os.path.isfile(image_path):
                tk.messagebox.showinfo("Error", "The path {} is not a valid file".format(image_path))
                return
            if not image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                tk.messagebox.showinfo("Error", "The path {} is not a valid image file".format(image_path))
                return
            image = Image.open(image_path)
            self.original_image = image.copy()
            self.image_size = image.size
            self.processed_image = None
            if not self.using_transformations:
                self.display_image(image)
            else:
                self.using_transformations()

    def display_image(self, image, resize=True):
        if resize:
            image = resize_image(image, self.image_size, self.canvas.winfo_width(), self.canvas.winfo_height())

        photo = ImageTk.PhotoImage(image)

        # Calculate the position to center the image
        x = (self.canvas.winfo_width() - photo.width()) // 2
        y = (self.canvas.winfo_height() - photo.height()) // 2

        self.canvas.config(width=photo.width(), height=photo.height())
        self.canvas.create_image(x, y, anchor=tk.NW, image=photo)
        self.canvas.image = photo

    def compare_images(self, image1, image2):
        image1 = resize_image(image1, self.image_size, self.canvas.winfo_width(), self.canvas.winfo_height())
        print(image1.size)
        image2 = resize_image(image2, self.image_size, self.canvas.winfo_width(), self.canvas.winfo_height())
        width = image1.width + 100 + image2.width
        print(width)
        height = max(image1.height, image2.height)
        system_button_face_rgb = root.winfo_rgb('SystemButtonFace')
        new_image = Image.new("RGBA", (width, height), color=tuple(x // 256 for x in system_button_face_rgb))
        new_image.paste(image1, (0, 0))
        new_image.paste(image2, (image1.width + 100, 0))
        self.display_image(new_image, resize=False)

    def save_image(self):
        if self.processed_image:
            # Get the directory to save the image
            filename = filedialog.asksaveasfilename(initialdir=self.current_directory,
                                                    title="Select file",
                                                    filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
            if filename:
                # extend the filename if the user did not add the extension
                if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    filename += ".jpg"
                self.processed_image.save(filename)
        else:
            tk.messagebox.showinfo("Error", "No processed image to save")

    def default(self):
        self.using_transformations = None
        self.display_image(self.original_image)

    def blur_image(self):
        if self.original_image:
            self.using_transformations = self.blur_image
            self.processed_image = self.original_image.filter(ImageFilter.BLUR)
            self.compare_images(self.original_image, self.processed_image)
        else:
            tk.messagebox.showinfo("Error", "No image loaded")

    def exp_grayscale(self):
        if self.original_image:
            self.using_transformations = self.exp_grayscale
            self.processed_image = power_law_image(self.original_image, 1.5, 1)
            self.compare_images(self.original_image, self.processed_image)
        else:
            tk.messagebox.showinfo("Error", "No image loaded")

    def gamma_correction(self):
        if self.original_image:
            self.using_transformations = self.gamma_correction
            self.processed_image = gamma_correction(self.original_image, 0.8, 10)
            self.compare_images(self.original_image, self.processed_image)
        else:
            tk.messagebox.showinfo("Error", "No image loaded")

    def hist_qualization(self):
        if self.original_image:
            self.using_transformations = self.hist_qualization
            self.processed_image = Image.fromarray(Histogram.equalization(np.array(self.original_image)))
            self.compare_images(self.original_image, self.processed_image)
        else:
            tk.messagebox.showinfo("Error", "No image loaded")

    def mod_window_before_mean_filter(self):
        # Create a frame to hold the kernel size bar and buttons
        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP, pady=10)

        # Label and Scale for kernel size
        label = tk.Label(frame, text="Select Kernel Size:")
        label.pack(side=tk.LEFT, padx=10)

        kernel_size_var = tk.IntVar()
        kernel_size_scale = tk.Scale(frame, from_=1, to=15, orient=tk.HORIZONTAL, variable=kernel_size_var,
                                     resolution=2)
        kernel_size_scale.pack(side=tk.LEFT, padx=10)

        return kernel_size_scale, frame

    def mean_filter(self):
        if self.original_image:
            self.using_transformations = self.mean_filter
            kernel_size_scale, frame = self.mod_window_before_mean_filter()

            # Schedule the update function to run after 300 milliseconds
            self.root.after(300, self.update_mean_filter, kernel_size_scale, frame)
        else:
            tk.messagebox.showinfo("Error", "No image loaded")

    def update_mean_filter(self, kernel_size_scale, frame):
        if self.using_transformations == self.mean_filter:
            # Get the kernel size from the scale
            kernel_size = kernel_size_scale.get()

            # Perform the mean filter operation
            self.processed_image = mean_filter(self.original_image, kernel_size)

            # Display the original and processed images
            self.compare_images(self.original_image, self.processed_image)

            # Schedule the next update after 300 milliseconds
            self.root.after(300, self.update_mean_filter, kernel_size_scale, frame)
        else:
            # Remove the kernel size bar and buttons
            frame.destroy()

    ####Add noise Here
    def Add_noise(self, type):
        Noise = Addnoise()
        if self.original_image:
            self.using_transformations = self.Add_noise
            if type == "Gaussian":
                self.processed_image = Image.fromarray(Noise.gauss(np.array(self.original_image)))
            elif type == "Salt Pepper":
                self.processed_image = Image.fromarray(Noise.sp_noise(np.array(self.original_image)))
            elif type == "Gamma":
                self.processed_image = Image.fromarray(Noise.gamma_noise(np.array(self.original_image)))
            elif type == "Uniform":
                self.processed_image = Image.fromarray(Noise.uniform_noise(np.array(self.original_image)))
            elif type == "Exponential":
                self.processed_image = Image.fromarray(Noise.exponential_noise(np.array(self.original_image)))
            elif type == "Rayleigh":
                self.processed_image = Image.fromarray(Noise.rayl_noise(np.array(self.original_image)))
            self.compare_images(self.original_image, self.processed_image)
        else:
            tk.messagebox.showinfo("Error", "No image loaded")

    # def para_window(self, func_name):
    #     # 创建弹出窗口
    #     popup = tk.Toplevel(root)
    #     popup.title("Parameters")
    #     popup.geometry("200x150")
    #
    #     def execFunc(func_name):
    #         ##TODO:根据函数名获取函数参数个数并传参，然后执行对应函数
    #
    #         pass
    #
    #     button = tk.Button(popup, text="ok", command=partial(execFunc, func_name))
    #     button.pack()
    #     button = tk.Button(popup, text="exit", command=popup.destroy)
    #     button.pack()

    def show_previous_image(self):
        if self.image_list:
            self.current_index = (self.current_index - 1) % len(self.image_list)
            self.load_current_image()

    def show_next_image(self):
        if self.image_list:
            self.current_index = (self.current_index + 1) % len(self.image_list)
            self.load_current_image()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
