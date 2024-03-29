import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter
from image_transform import *
from support import *
from equalizeHist import *
from addnoise import *
from fourier import *
from recovery import *
from functools import partial
import threading


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        self.tid = 0
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
        menubar.add_cascade(label="Image Processing", menu=process_menu)
        process_menu.add_command(label="Default", command=self.default)
        process_menu.add_command(label="Blur", command=self.blur_image)
        process_menu.add_command(label="Exponential grayscale transformation", command=self.exp_grayscale)
        process_menu.add_command(label="Gamma correction", command=self.gamma_correction)
        process_menu.add_command(label="Mean filter", command=self.mean_filter)
        process_menu.add_command(label="Median filter", command=self.median_filter)
        process_menu.add_command(label="Invert", command=self.invert)
        process_menu.add_command(label="Laplace filter", command=self.laplace_filter)
        process_menu.add_command(label="Histogram equalization", command=self.hist_qualization)

        # Fourier Transform Options
        Fourier_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fourier Analysis", menu=Fourier_menu)
        Fourier_menu.add_command(label="Spectrum", command=self.fourier_spectrum)
        Fourier_menu.add_command(label="Gaussian low pass filter", command=self.g_low_pass_filter)
        Fourier_menu.add_command(label="Gaussian high pass filter", command=self.g_high_pass_filter)
        Fourier_menu.add_command(label="Butterworth low pass filter", command=self.b_low_pass_filter)
        Fourier_menu.add_command(label="Butterworth high pass filter", command=self.b_high_pass_filter)

        # Image recovery Options
        recovery_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Image recovery", menu=recovery_menu)
        recovery_menu.add_command(label="Inverse filter", command=self.inverse_filter)
        recovery_menu.add_command(label="Wiener filter", command=self.wiener_filter)

        # Add noise Options
        Noise_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Add noise", menu=Noise_menu)
        Noise_menu.add_command(label="Default", command=self.default)
        Noise_menu.add_command(label="Gaussian", command=partial(self.Add_noise_type, "Gaussian"))
        Noise_menu.add_command(label="Salt Pepper", command=partial(self.Add_noise_type, "Salt Pepper"))
        Noise_menu.add_command(label="Gamma", command=partial(self.Add_noise_type, "Gamma"))
        Noise_menu.add_command(label="Uniform", command=partial(self.Add_noise_type, "Uniform"))
        Noise_menu.add_command(label="Exponential", command=partial(self.Add_noise_type, "Exponential"))
        Noise_menu.add_command(label="Rayleigh", command=partial(self.Add_noise_type, "Rayleigh"))

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
        self.last_image = self.original_image

        self.cache1 = None
        self.cache2 = None

    def open_image(self):
        self.current_directory = filedialog.askdirectory()
        if self.current_directory:
            self.image_list = [f for f in os.listdir(self.current_directory) if
                               f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
            if not self.image_list:
                tk.messagebox.showinfo("Error", "The directory {} does not contain any images, please check your "
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
            # Convert the image to RGB format
            image = image.convert('RGB')
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
        image2 = resize_image(image2, self.image_size, self.canvas.winfo_width(), self.canvas.winfo_height())
        width = image1.width + 100 + image2.width
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
        try:
            if len(self.root.winfo_children()) >= 4:
                frame = self.root.winfo_children()[3]
                frame.destroy()
        except:
            pass


    def blur_image(self):
        self.default()
        if self.original_image:
            self.using_transformations = self.blur_image
            self.processed_image = self.original_image.filter(ImageFilter.BLUR)
            self.compare_images(self.original_image, self.processed_image)
        else:
            tk.messagebox.showinfo("Error", "No image loaded")

    def mod_window_before_exp_grayscale(self):
        if self.using_transformations != self.exp_grayscale:
            # Create a frame to hold the kernel size bar and buttons
            frame = tk.Frame(self.root)
            frame.pack(side=tk.TOP, pady=10)

            # Label and Scale for kernel size
            label = tk.Label(frame, text="Select Gamma:")
            label.pack(side=tk.LEFT, padx=10)

            gamma_var = tk.IntVar()
            gamma_scale = tk.Scale(frame, from_=0.2, to=5, orient=tk.HORIZONTAL, variable=gamma_var,
                                   resolution=0.1)
            gamma_scale.pack(side=tk.LEFT, padx=10)
        else:
            # find the frame that holds the kernel size bar and buttons
            # print(self.root.winfo_children())
            frame = self.root.winfo_children()[3]
            gamma_scale = frame.winfo_children()[1]

        return gamma_scale, frame

    def exp_grayscale(self):
        self.default()
        if self.original_image:
            gamma_scale, frame = self.mod_window_before_exp_grayscale()
            self.using_transformations = self.exp_grayscale
            self.cache1 = gamma_scale

            # Schedule the update function to run after 100 milliseconds
            t = self.root.after(100, self.update_exp_grayscale, gamma_scale, frame)
            self.tid = t

        else:
            tk.messagebox.showinfo("Error", "No image loaded")

    def update_exp_grayscale(self, gamma_scale, frame):
        if self.using_transformations == self.exp_grayscale:
            # fast skip
            if self.cache1 == gamma_scale.get():
                # Schedule the next update after 300 milliseconds
                t = self.root.after(300, self.update_exp_grayscale, gamma_scale, frame)
                self.tid = t
                return

            # Get the kernel size from the scale
            self.cache1 = gamma = gamma_scale.get()

            # Perform the mean filter operation
            self.processed_image = power_law_image(self.original_image, gamma, 1)

            # Display the original and processed images
            self.compare_images(self.original_image, self.processed_image)

            # Schedule the next update after 100 milliseconds
            t = self.root.after(100, self.update_exp_grayscale, gamma_scale, frame)
            self.tid = t
            return

        else:
            # Remove the kernel size bar and buttons
            frame.destroy()
            return


    def mod_window_before_gamma_correction(self):
        if self.using_transformations != self.gamma_correction:
            # Create a frame to hold the kernel size bar and buttons
            frame = tk.Frame(self.root)
            frame.pack(side=tk.TOP, pady=10)

            # Label and Scale for gamma value
            label = tk.Label(frame, text="Select Gamma:")
            label.pack(side=tk.LEFT, padx=10)

            gamma_var = tk.IntVar()
            gamma_scale = tk.Scale(frame, from_=0.5, to=1.2, orient=tk.HORIZONTAL, variable=gamma_var,
                                   resolution=0.03)
            gamma_scale.pack(side=tk.LEFT, padx=10)
        else:
            # print(self.root.winfo_children())
            frame = self.root.winfo_children()[3]
            gamma_scale = frame.winfo_children()[1]

        return gamma_scale, frame

    def gamma_correction(self):
        self.default()
        if self.original_image:
            gamma_scale, frame = self.mod_window_before_gamma_correction()
            self.using_transformations = self.gamma_correction
            self.cache1 = gamma_scale

            # Schedule the update function to run after 100 milliseconds
            t = self.root.after(100, self.update_gamma_correction, gamma_scale, frame)
            self.tid = t

    def update_gamma_correction(self, gamma_scale, frame):
        if self.using_transformations == self.gamma_correction:
            # fast skip
            if self.cache1 == gamma_scale.get():
                # Schedule the next update after 300 milliseconds
                t = self.root.after(300, self.update_gamma_correction, gamma_scale, frame)
                self.tid = t
                return

            # Get the kernel size from the scale
            self.cache1 = gamma = gamma_scale.get()

            # Perform the mean filter operation
            self.processed_image = gamma_correction(self.original_image, gamma, 10)

            # Display the original and processed images
            self.compare_images(self.original_image, self.processed_image)

            # Schedule the next update after 100 milliseconds
            t = self.root.after(100, self.update_gamma_correction, gamma_scale, frame)
            self.tid = t
            return

        else:
            # Remove the kernel size bar and buttons
            frame.destroy()
            return

    def hist_qualization(self):
        self.default()
        if self.original_image:
            self.using_transformations = self.hist_qualization
            H = Histogram()
            self.processed_image = Image.fromarray(H.equalization(np.array(self.original_image)))
            self.compare_images(self.original_image, self.processed_image)
        else:
            tk.messagebox.showinfo("Error", "No image loaded")

    def mod_window_before_mean_filter(self):
        if self.using_transformations != self.mean_filter:
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
        else:
            # find the frame that holds the kernel size bar and buttons
            # print(self.root.winfo_children())
            frame = self.root.winfo_children()[3]
            kernel_size_scale = frame.winfo_children()[1]

        return kernel_size_scale, frame

    def mean_filter(self):
        self.default()
        if self.original_image:
            kernel_size_scale, frame = self.mod_window_before_mean_filter()
            self.cache1 = kernel_size_scale
            self.using_transformations = self.mean_filter

            # Schedule the update function to run after 100 milliseconds
            t = self.root.after(100, self.update_mean_filter, kernel_size_scale, frame)
            self.tid = t


        else:
            tk.messagebox.showinfo("Error", "No image loaded")

    def update_mean_filter(self, kernel_size_scale, frame):
        if self.using_transformations == self.mean_filter:
            # fast skip
            if self.cache1 == kernel_size_scale.get():
                # Schedule the next update after 300 milliseconds
                t = self.root.after(300, self.update_mean_filter, kernel_size_scale, frame)
                self.tid = t
                return

            # Get the kernel size from the scale
            self.cache1 = kernel_size = kernel_size_scale.get()

            # Perform the mean filter operation
            self.processed_image = mean_filter(self.original_image, kernel_size)

            # Display the original and processed images
            self.compare_images(self.original_image, self.processed_image)

            # Schedule the next update after 100 milliseconds
            t = self.root.after(100, self.update_mean_filter, kernel_size_scale, frame)
            self.tid = t
            return

        else:
            # Remove the kernel size bar and buttons
            frame.destroy()
            return

    def mod_window_before_median_filter(self):
        if self.using_transformations != self.median_filter:
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
        else:
            # find the frame that holds the kernel size bar and buttons
            # print(self.root.winfo_children())
            frame = self.root.winfo_children()[3]
            kernel_size_scale = frame.winfo_children()[1]

        return kernel_size_scale, frame

    def median_filter(self):
        self.default()
        if self.original_image:
            kernel_size_scale, frame = self.mod_window_before_median_filter()
            self.using_transformations = self.median_filter
            self.cache1 = kernel_size_scale

            # Schedule the update function to run after 100 milliseconds
            t = self.root.after(100, self.update_median_filter, kernel_size_scale, frame)
            self.tid = t

        else:
            tk.messagebox.showinfo("Error", "No image loaded")

    def update_median_filter(self, kernel_size_scale, frame):
        # fast skip
        if self.cache1 == kernel_size_scale.get():
            # Schedule the next update after 300 milliseconds
            t = self.root.after(300, self.update_median_filter, kernel_size_scale, frame)
            self.tid = t
            return
        if self.using_transformations == self.median_filter:
            # Get the kernel size from the scale
            kernel_size = kernel_size_scale.get()

            # Perform the median filter operation
            self.processed_image = median_filter(self.original_image, kernel_size)

            # Display the original and processed images
            self.compare_images(self.original_image, self.processed_image)

            # Schedule the next update after 100 milliseconds
            t = self.root.after(100, self.update_median_filter, kernel_size_scale, frame)
            self.tid = t

        else:
            # Remove the kernel size bar and buttons
            frame.destroy()

    def invert(self):
        self.default()
        if self.original_image:
            self.using_transformations = self.invert
            self.processed_image = invert(self.original_image)
            self.compare_images(self.original_image, self.processed_image)
        else:
            tk.messagebox.showinfo("Error", "No image loaded")

    def mod_window_before_laplace_filter(self):
        # add a switch to let the user choose between two laplace filters
        if self.using_transformations != self.laplace_filter:
            # Create a frame to hold the kernel size bar and buttons
            frame = tk.Frame(self.root)
            frame.pack(side=tk.TOP, pady=10)

            # Label and Scale for kernel type
            label = tk.Label(frame, text="Select Kernel Type:")
            label.pack(side=tk.LEFT, padx=10)

            kernel_type_var = tk.IntVar()
            kernel_type_scale = tk.Scale(frame, from_=1, to=2, orient=tk.HORIZONTAL, variable=kernel_type_var)
            kernel_type_scale.pack(side=tk.LEFT, padx=10)
        else:
            # find the frame that holds the kernel type bar and buttons
            frame = self.root.winfo_children()[3]
            kernel_type_scale = frame.winfo_children()[3]
        return kernel_type_scale, frame

    def laplace_filter(self):
        self.default()
        if self.original_image:
            kernel_type_scale, frame = self.mod_window_before_laplace_filter()
            self.using_transformations = self.laplace_filter
            self.cache1 = kernel_type_scale

            # Schedule the update function to run after 100 milliseconds
            t = self.root.after(100, self.update_laplace_filter, kernel_type_scale, frame)
            self.tid = t

        else:
            tk.messagebox.showinfo("Error", "No image loaded")

    def update_laplace_filter(self, kernel_type_scale, frame):
        if self.using_transformations == self.laplace_filter:
            # Get the kernel type from the scale
            kernel_type = kernel_type_scale.get()

            if self.cache1 == kernel_type:
                # Schedule the next update after 300 milliseconds
                t = self.root.after(300, self.update_laplace_filter, kernel_type_scale, frame)
                self.tid = t
                return

            # Perform the laplace filter operation
            if kernel_type == 1:
                self.processed_image = laplace_filter(self.original_image, laplace_core1)
            else:
                self.processed_image = laplace_filter(self.original_image, laplace_core2)

            # Display the original and processed images
            self.compare_images(self.original_image, self.processed_image)

            # Schedule the next update after 100 milliseconds
            t = self.root.after(100, self.update_laplace_filter, kernel_type_scale, frame)
            self.tid = t
            return

        else:
            # Remove the kernel type bar and buttons
            frame.destroy()
            return

    ####Add noise Here
    def Add_noise_type(self,type):
        self.noisetype=type
        self.Add_noise()
    def Add_noise_before(self):
        if self.using_transformations != self.Add_noise:
            frame = tk.Frame(self.root)
            frame.pack(side=tk.TOP, pady=10)
        else:
            frame = self.root.winfo_children()[3]
        return frame
    def Add_noise(self):
        frame=self.Add_noise_before()
        Noise = Addnoise()
        if self.original_image:

            if self.noisetype == "Gaussian":
                # Label and Scale for kernel size
                for widget in frame.winfo_children():
                    widget.destroy()
                label = tk.Label(frame, text="enter mean:")
                label.pack()
                mean_e = tk.Entry(frame)
                mean_e.pack()
                label = tk.Label(frame, text="enter var:")
                label.pack()
                var_e = tk.Entry(frame)
                var_e.pack()
                def mymodify():
                  try:
                    self.processed_image = Image.fromarray(
                        Noise.gauss(np.array(self.original_image), float(mean_e.get()), float(var_e.get())))
                    self.compare_images(self.original_image, self.processed_image)
                    messagebox.showinfo("success", "Success!")
                  except Exception as a:
                      messagebox.showerror("Error", "Wrong input")
                button = tk.Button(frame, text="ok", command=mymodify)
                button.pack()


                self.processed_image = Image.fromarray(Noise.gauss(np.array(self.original_image)))


            elif  self.noisetype == "Salt Pepper":
                # Label and Scale for kernel size
                for widget in frame.winfo_children():
                    widget.destroy()
                label = tk.Label(frame, text="enter amount (0~1):")
                label.pack()
                e = tk.Entry(frame)
                e.pack()

                def mymodify():
                  try:
                    self.processed_image = Image.fromarray(
                        Noise.sp_noise(np.array(self.original_image), float(e.get())))
                    self.compare_images(self.original_image, self.processed_image)
                    messagebox.showinfo("success", "Success!")
                  except Exception as a:
                      messagebox.showerror("Error", "Wrong input")

                button = tk.Button(frame, text="ok", command=mymodify)
                button.pack()


                self.processed_image = Image.fromarray(Noise.sp_noise(np.array(self.original_image)))

            elif  self.noisetype == "Gamma":
                for widget in frame.winfo_children():
                    widget.destroy()
                label = tk.Label(frame, text="enter scale:")
                label.pack()
                e = tk.Entry(frame)
                e.pack()

                def mymodify():
                   try:
                    self.processed_image = Image.fromarray(
                        Noise.gamma_noise(np.array(self.original_image), float(e.get())))
                    self.compare_images(self.original_image, self.processed_image)
                    messagebox.showinfo("success", "Success!")
                   except Exception as a:
                       messagebox.showerror("Error", "Wrong input")

                button = tk.Button(frame, text="ok", command=mymodify)
                button.pack()


                self.processed_image = Image.fromarray(Noise.gamma_noise(np.array(self.original_image)))

            elif  self.noisetype == "Uniform":
                for widget in frame.winfo_children():
                    widget.destroy()
                label = tk.Label(frame, text="enter low (0~1):")
                label.pack()
                e1 = tk.Entry(frame)
                e1.pack()
                label = tk.Label(frame, text="enter high (0~1):")
                label.pack()
                e2 = tk.Entry(frame)
                e2.pack()
                def mymodify():
                   try:
                    self.processed_image = Image.fromarray(
                        Noise.uniform_noise(np.array(self.original_image), float(e1.get()), float(e2.get())))
                    self.compare_images(self.original_image, self.processed_image)
                    messagebox.showinfo("success", "Success!")
                   except Exception as a:
                       messagebox.showerror("Error", "Wrong input")

                button = tk.Button(frame, text="ok", command=mymodify)
                button.pack()
                self.processed_image = Image.fromarray(Noise.uniform_noise(np.array(self.original_image)))

            elif  self.noisetype == "Exponential":
                for widget in frame.winfo_children():
                    widget.destroy()
                label = tk.Label(frame, text="enter scale(0-1):")
                label.pack()
                e = tk.Entry(frame)
                e.pack()
                def mymodify():
                  try:
                    self.processed_image = Image.fromarray(
                        Noise.exponential_noise(np.array(self.original_image), float(e.get())))
                    self.compare_images(self.original_image, self.processed_image)
                    messagebox.showinfo("success", "Success!")
                  except Exception as a:
                    messagebox.showerror("Error", "Wrong input")

                button = tk.Button(frame, text="ok", command=mymodify)
                button.pack()
                self.processed_image = Image.fromarray(Noise.exponential_noise(np.array(self.original_image)))

            elif  self.noisetype == "Rayleigh":
                for widget in frame.winfo_children():
                    widget.destroy()
                label = tk.Label(frame, text="enter scale (0~1):")
                label.pack()
                e = tk.Entry(frame)
                e.pack()

                def mymodify():
                  try:
                    self.processed_image = Image.fromarray(
                        Noise.rayl_noise(np.array(self.original_image), float(e.get())))
                    self.compare_images(self.original_image, self.processed_image)
                    messagebox.showinfo("success", "Success!")
                  except Exception as a:
                    messagebox.showerror("Error", "Wrong input")



                button = tk.Button(frame, text="ok", command=mymodify)
                button.pack()
                self.processed_image = Image.fromarray(Noise.rayl_noise(np.array(self.original_image)))


            if  self.processed_image:
               self.compare_images(self.original_image, self.processed_image)
            self.using_transformations = self.Add_noise

        else:
            tk.messagebox.showinfo("Error", "No image loaded")

    def fourier_spectrum(self):
        self.default()
        if self.original_image:
            self.using_transformations = self.fourier_spectrum
            self.processed_image = fourier_transform(self.original_image)
            self.compare_images(self.original_image, self.processed_image)
        else:
            tk.messagebox.showinfo("Error", "No image loaded")

    def mod_window_before_g_low_pass_filter(self):
        if self.using_transformations != self.g_low_pass_filter:
            # Create a frame to hold the kernel size bar and buttons
            frame = tk.Frame(self.root)
            frame.pack(side=tk.TOP, pady=10)

            # Label and Scale for sigma
            label = tk.Label(frame, text="Select ln(sigma):")
            label.pack(side=tk.LEFT, padx=10)

            sigma_var = tk.DoubleVar()
            sigma_scale = tk.Scale(frame, from_=-2, to=6, orient=tk.HORIZONTAL, variable=sigma_var,
                                   resolution=0.05)
            sigma_scale.pack(side=tk.LEFT, padx=10)
        else:
            # find the frame that holds the kernel size bar and buttons
            # print(self.root.winfo_children())
            frame = self.root.winfo_children()[3]
            sigma_scale = frame.winfo_children()[1]

        return sigma_scale, frame

    def g_low_pass_filter(self):
        self.default()
        if self.original_image:
            sigma_scale, frame = self.mod_window_before_g_low_pass_filter()
            self.using_transformations = self.g_low_pass_filter
            self.cache1 = sigma_scale

            # Schedule the update function to run after 100 milliseconds
            t = self.root.after(100, self.update_g_low_pass_filter, sigma_scale, frame)
            self.tid = t

        else:
            tk.messagebox.showinfo("Error", "No image loaded")

    def update_g_low_pass_filter(self, sigma_scale, frame):
        self.default()
        if self.using_transformations == self.g_low_pass_filter:
            # fast skip
            if self.cache1 == sigma_scale.get():
                # Schedule the next update after 300 milliseconds
                t = self.root.after(300, self.update_g_low_pass_filter, sigma_scale, frame)
                self.tid = t
                return

            # Get the sigma from the scale
            sigma = sigma_scale.get()

            # Perform the gaussian low pass filter operation
            self.processed_image = gaussian_low_pass_filter(self.original_image, sigma)

            # Display the original and processed images
            self.compare_images(self.original_image, self.processed_image)

            # Schedule the next update after 100 milliseconds
            t = self.root.after(100, self.update_g_low_pass_filter, sigma_scale, frame)
            self.tid = t
            return

        else:
            # Remove the sigma bar and buttons
            frame.destroy()
            return

    def mod_window_before_g_high_pass_filter(self):
        if self.using_transformations != self.g_high_pass_filter:
            # Create a frame to hold the kernel size bar and buttons
            frame = tk.Frame(self.root)
            frame.pack(side=tk.TOP, pady=10)

            # Label and Scale for sigma
            label = tk.Label(frame, text="Select ln(sigma):")
            label.pack(side=tk.LEFT, padx=10)

            sigma_var = tk.DoubleVar()
            sigma_scale = tk.Scale(frame, from_=-2, to=6, orient=tk.HORIZONTAL, variable=sigma_var,
                                   resolution=0.05)
            sigma_scale.pack(side=tk.LEFT, padx=10)
        else:
            # find the frame that holds the kernel size bar and buttons
            # print(self.root.winfo_children())
            frame = self.root.winfo_children()[3]
            sigma_scale = frame.winfo_children()[1]

        return sigma_scale, frame

    def g_high_pass_filter(self):
        self.default()
        if self.original_image:
            sigma_scale, frame = self.mod_window_before_g_high_pass_filter()
            self.using_transformations = self.g_high_pass_filter
            self.cache1 = sigma_scale

            # Schedule the update function to run after 100 milliseconds
            t = self.root.after(100, self.update_g_high_pass_filter, sigma_scale, frame)
            self.tid = t

        else:
            tk.messagebox.showinfo("Error", "No image loaded")

    def update_g_high_pass_filter(self, sigma_scale, frame):
        if self.using_transformations == self.g_high_pass_filter:
            # fast skip
            if self.cache1 == sigma_scale.get():
                # Schedule the next update after 300 milliseconds
                t = self.root.after(300, self.update_g_high_pass_filter, sigma_scale, frame)
                self.tid = t
                return
            # Get the sigma from the scale
            sigma = sigma_scale.get()

            # Perform the gaussian high pass filter operation
            self.processed_image = gaussian_high_pass_filter(self.original_image, sigma)

            # Display the original and processed images
            self.compare_images(self.original_image, self.processed_image)

            # Schedule the next update after 100 milliseconds
            t = self.root.after(100, self.update_g_high_pass_filter, sigma_scale, frame)
            self.tid = t

        else:
            # Remove the sigma bar and buttons
            frame.destroy()

    def mod_window_before_b_low_pass_filter(self):
        if self.using_transformations != self.b_low_pass_filter:
            # Create a frame to hold the kernel size bar and buttons
            frame = tk.Frame(self.root)
            frame.pack(side=tk.TOP, pady=10)

            # Label and Scale for order
            label = tk.Label(frame, text="Select order:")
            label.pack(side=tk.LEFT, padx=10)

            order_var = tk.IntVar()
            order_scale = tk.Scale(frame, from_=1, to=2, orient=tk.HORIZONTAL, variable=order_var,
                                   resolution=1)
            order_scale.pack(side=tk.LEFT, padx=10)

            # Label and Scale for cutoff frequency
            label = tk.Label(frame, text="Select cutoff:")
            label.pack(side=tk.LEFT, padx=10)

            cutoff_var = tk.DoubleVar()
            cutoff_scale = tk.Scale(frame, from_=.01, to=.49, orient=tk.HORIZONTAL, variable=cutoff_var,
                                    resolution=.01)
            cutoff_scale.pack(side=tk.LEFT, padx=10)
        else:
            # find the frame that holds the kernel size bar and buttons
            # print(self.root.winfo_children())
            frame = self.root.winfo_children()[3]
            order_scale = frame.winfo_children()[1]
            cutoff_scale = frame.winfo_children()[3]

        return order_scale, cutoff_scale, frame

    def b_low_pass_filter(self):
        self.default()
        if self.original_image:
            order_scale, cutoff_scale, frame = self.mod_window_before_b_low_pass_filter()
            self.using_transformations = self.b_low_pass_filter
            self.cache1 = int(order_scale.get())
            self.cache2 = cutoff_scale

            # Schedule the update function to run after 100 milliseconds
            t = self.root.after(100, self.update_b_low_pass_filter, order_scale, cutoff_scale, frame)
            self.tid = t

        else:
            tk.messagebox.showinfo("Error", "No image loaded")

    def update_b_low_pass_filter(self, order_scale, cutoff_scale, frame):
        if self.using_transformations == self.b_low_pass_filter:
            # Get the order and cutoff frequency from the scale
            order = int(order_scale.get())
            cutoff = cutoff_scale.get()

            # fast skip
            if self.cache1 == order and self.cache2 == cutoff:
                # Schedule the next update after 300 milliseconds
                t = self.root.after(300, self.update_b_low_pass_filter, order_scale, cutoff_scale, frame)
                self.tid = t
                return

            # Perform the butterworth low pass filter operation
            self.processed_image = butterworth_low_pass_filter(self.original_image, order=order,
                                                               cutoff_frequency=cutoff)

            # Display the original and processed images
            self.compare_images(self.original_image, self.processed_image)

            # Schedule the next update after 100 milliseconds
            t = self.root.after(100, self.update_b_low_pass_filter, order_scale, cutoff_scale, frame)
            self.tid = t

        else:
            # Remove the order and cutoff frequency bar and buttons
            frame.destroy()

    def mod_window_before_b_high_pass_filter(self):
        if self.using_transformations != self.b_high_pass_filter:
            # Create a frame to hold the kernel size bar and buttons
            frame = tk.Frame(self.root)
            frame.pack(side=tk.TOP, pady=10)

            # Label and Scale for order
            label = tk.Label(frame, text="Select order:")
            label.pack(side=tk.LEFT, padx=10)

            order_var = tk.IntVar()
            order_scale = tk.Scale(frame, from_=1, to=2, orient=tk.HORIZONTAL, variable=order_var,
                                   resolution=1)
            order_scale.pack(side=tk.LEFT, padx=10)

            # Label and Scale for cutoff frequency
            label = tk.Label(frame, text="Select cutoff:")
            label.pack(side=tk.LEFT, padx=10)

            cutoff_var = tk.DoubleVar()
            cutoff_scale = tk.Scale(frame, from_=.01, to=.49, orient=tk.HORIZONTAL, variable=cutoff_var,
                                    resolution=.01)
            cutoff_scale.pack(side=tk.LEFT, padx=10)
        else:
            # find the frame that holds the kernel size bar and buttons
            # print(self.root.winfo_children())
            frame = self.root.winfo_children()[3]
            order_scale = frame.winfo_children()[1]
            cutoff_scale = frame.winfo_children()[3]

        return order_scale, cutoff_scale, frame

    def b_high_pass_filter(self):
        self.default()
        if self.original_image:
            order_scale, cutoff_scale, frame = self.mod_window_before_b_high_pass_filter()
            self.using_transformations = self.b_high_pass_filter
            self.cache1 = int(order_scale.get())
            self.cache2 = cutoff_scale
            # Schedule the update function to run after 100 milliseconds
            t = self.root.after(100, self.update_b_high_pass_filter, order_scale, cutoff_scale, frame)
            self.tid = t

        else:
            tk.messagebox.showinfo("Error", "No image loaded")

    def update_b_high_pass_filter(self, order_scale, cutoff_scale, frame):
        if self.using_transformations == self.b_high_pass_filter:
            # Get the order and cutoff frequency from the scale
            order = int(order_scale.get())
            cutoff = cutoff_scale.get()

            # fast skip
            if self.cache1 == order and self.cache2 == cutoff:
                # Schedule the next update after 300 milliseconds
                t = self.root.after(300, self.update_b_high_pass_filter, order_scale, cutoff_scale, frame)
                self.tid = t
                return

            # Perform the butterworth high pass filter operation
            self.processed_image = butterworth_high_pass_filter(self.original_image, order=order,
                                                                cutoff_frequency=cutoff)

            # Display the original and processed images
            self.compare_images(self.original_image, self.processed_image)

            # Schedule the next update after 100 milliseconds
            t = self.root.after(100, self.update_b_high_pass_filter, order_scale, cutoff_scale, frame)
            self.tid = t

        else:
            # Remove the order and cutoff frequency bar and buttons
            frame.destroy()

    def mod_window_before_inverse_filter(self):
        if self.using_transformations != self.inverse_filter:
            # Create a frame to hold the kernel size bar and buttons
            frame = tk.Frame(self.root)
            frame.pack(side=tk.TOP, pady=10)

            # Label and Scale for k value
            label = tk.Label(frame, text="Select k value:")
            label.pack(side=tk.LEFT, padx=10)

            k_var = tk.DoubleVar()
            k_scale = tk.Scale(frame, from_=0, to=1, orient=tk.HORIZONTAL, variable=k_var,
                               resolution=.01)
            k_scale.pack(side=tk.LEFT, padx=10)
        else:
            # find the frame that holds the kernel size bar and buttons
            # print(self.root.winfo_children())
            frame = self.root.winfo_children()[3]
            k_scale = frame.winfo_children()[1]

        return k_scale, frame

    def inverse_filter(self):
        self.default()
        if self.original_image:
            k_scale, frame = self.mod_window_before_inverse_filter()
            self.using_transformations = self.inverse_filter
            self.cache1 = k_scale

            # Schedule the update function to run after 100 milliseconds
            t = self.root.after(100, self.update_inverse_filter, k_scale, frame)
            self.tid = t

        else:
            tk.messagebox.showinfo("Error", "No image loaded")

    def update_inverse_filter(self, k_scale, frame):
        if self.using_transformations == self.inverse_filter:
            # Get the k value from the scale
            k = k_scale.get()

            # fast skip
            if self.cache1 == k:
                # Schedule the next update after 300 milliseconds
                t = self.root.after(300, self.update_inverse_filter, k_scale, frame)
                self.tid = t
                return

            # Perform the inverse filter operation
            self.processed_image = inverse_filter(self.original_image, k)

            # Display the original and processed images
            self.compare_images(self.original_image, self.processed_image)

            # Schedule the next update after 100 milliseconds
            t = self.root.after(100, self.update_inverse_filter, k_scale, frame)
            self.tid = t

        else:
            # Remove the k value bar and buttons
            frame.destroy()

    def mod_window_before_wiener_filter(self):
        if self.using_transformations != self.wiener_filter:
            # Create a frame to hold the kernel size bar and buttons
            frame = tk.Frame(self.root)
            frame.pack(side=tk.TOP, pady=10)

            # Label and Scale for k value
            label = tk.Label(frame, text="Select k value:")
            label.pack(side=tk.LEFT, padx=10)

            k_var = tk.DoubleVar()
            k_scale = tk.Scale(frame, from_=0, to=1, orient=tk.HORIZONTAL, variable=k_var,
                               resolution=.01)
            k_scale.pack(side=tk.LEFT, padx=10)

            # Label and Scale for gamma value
            label = tk.Label(frame, text="Select gamma value:")
            label.pack(side=tk.LEFT, padx=10)

            gamma_var = tk.DoubleVar()
            gamma_scale = tk.Scale(frame, from_=0, to=1, orient=tk.HORIZONTAL, variable=gamma_var,
                                   resolution=.01)
            gamma_scale.pack(side=tk.LEFT, padx=10)
        else:
            # find the frame that holds the kernel size bar and buttons
            # print(self.root.winfo_children())
            frame = self.root.winfo_children()[3]
            k_scale = frame.winfo_children()[1]
            gamma_scale = frame.winfo_children()[3]

        return k_scale, gamma_scale, frame

    def wiener_filter(self):
        self.default()
        if self.original_image:
            k_scale, gamma_scale, frame = self.mod_window_before_wiener_filter()
            self.using_transformations = self.wiener_filter
            self.cache1 = k_scale
            self.cache2 = gamma_scale

            # Schedule the update function to run after 100 milliseconds
            t = self.root.after(100, self.update_wiener_filter, k_scale, gamma_scale, frame)
            self.tid = t

        else:
            tk.messagebox.showinfo("Error", "No image loaded")

    def update_wiener_filter(self, k_scale, gamma_scale, frame):
        if self.using_transformations == self.wiener_filter:
            # Get the k and gamma values from the scale
            k = k_scale.get()
            gamma = gamma_scale.get()

            # fast skip
            if self.cache1 == k and self.cache2 == gamma:
                # Schedule the next update after 300 milliseconds
                t = self.root.after(300, self.update_wiener_filter, k_scale, gamma_scale, frame)
                self.tid = t
                return

            # Perform the wiener filter operation
            self.processed_image = wiener_filter(self.original_image, k, gamma)

            # Display the original and processed images
            self.compare_images(self.original_image, self.processed_image)

            # Schedule the next update after 100 milliseconds
            t = self.root.after(100, self.update_wiener_filter, k_scale, gamma_scale, frame)
            self.tid = t

        else:
            # Remove the k and gamma value bar and buttons
            frame.destroy()



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
        self.default()
        if self.tid != 0:
            self.root.after_cancel(self.tid)
        if self.image_list:
            self.current_index = (self.current_index - 1) % len(self.image_list)
            self.load_current_image()

    def show_next_image(self):
        self.default()
        if self.tid != 0:
            self.root.after_cancel(self.tid)
        if self.image_list:
            self.current_index = (self.current_index + 1) % len(self.image_list)
            self.load_current_image()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)


    root.mainloop()
