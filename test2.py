def mod_window_before_gauss_noise(self):
    if self.using_transformations != self.gauss_noise:
        # Create a frame to hold the kernel size bar and buttons
        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP, pady=10)
        # Label and Scale for kernel size
        label = tk.Label(frame, text="Select mean:")
        label.pack(side=tk.LEFT, padx=10)
        mean_var = tk.DoubleVar()
        mean_scale = tk.Scale(frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL, variable=mean_var,
                              resolution=0.1)
        mean_scale.pack(side=tk.LEFT, padx=10)
        var_var = tk.DoubleVar()
        var_scale = tk.Scale(frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL, variable=var_var,
                             resolution=0.1)
        var_scale.pack(side=tk.LEFT, padx=10)
    else:
        # find the frame that holds the kernel size bar and buttons
        # print(self.root.winfo_children())
        frame = self.root.winfo_children()[3]
        mean_scale = frame.winfo_children()[1]
        var_scale = frame.winfo_children()[3]
    return mean_scale, var_scale, frame


def gauss_noise(self):
    if self.original_image:
        mean_scale, var_scale, frame = self.mod_window_before_gauss_noise()
        self.using_transformations = self.gauss_noise
        self.cache1 = mean_scale
        self.cache2 = var_scale
        # Schedule the update function to run after 100 milliseconds
        t = self.root.after(100, self.update_gauss_noise, mean_scale, var_scale, frame)
        self.tid = t

    else:
        tk.messagebox.showinfo("Error", "No image loaded")


def update_gauss_noise(self, mean_scale, var_scale, frame):
    addnoise = Addnoise()
    if self.using_transformations == self.gauss_noise:
        mean = mean_scale.get()
        var = var_scale.get()
        if self.cache1 == mean and self.cache2 == var:
            # Schedule the next update after 300 milliseconds
            t = self.root.after(300, self.update_gauss_noise, mean_scale, var_scale, frame)
            self.tid = t
            return
        # Perform the mean filter operation
        self.processed_image = addnoise.gauss(self.original_image, mean, var)
        # Display the original and processed images
        self.compare_images(self.original_image, self.processed_image)
        # Schedule the next update after 100 milliseconds
        t = self.root.after(100, self.update_gauss_noise, mean_scale, var_scale, frame)
        self.tid = t
        return
    else:
        # Remove the kernel size bar and buttons
        frame.destroy()
        return


def mod_window_before_uniform_noise(self):
    if self.using_transformations != self.uniform_noise:
        # Create a frame to hold the kernel size bar and buttons
        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP, pady=10)
        # Label and Scale for kernel size
        label = tk.Label(frame, text="Select mean:")
        label.pack(side=tk.LEFT, padx=10)
        low_var = tk.DoubleVar()
        low_scale = tk.Scale(frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL, variable=low_var,
                             resolution=0.1)
        low_scale.pack(side=tk.LEFT, padx=10)
        high_var = tk.DoubleVar()
        high_scale = tk.Scale(frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL, variable=high_var,
                              resolution=0.1)
        high_scale.pack(side=tk.LEFT, padx=10)
    else:
        # find the frame that holds the kernel size bar and buttons
        # print(self.root.winfo_children())
        frame = self.root.winfo_children()[3]
        low_scale = frame.winfo_children()[1]
        high_scale = frame.winfo_children()[3]
    return low_scale, high_scale, frame


def uniform_noise(self):
    if self.original_image:
        low_scale, high_scale, frame = self.mod_window_before_uniform_noise()
        self.using_transformations = self.uniform_noise
        self.cache1 = low_scale
        self.cache2 = high_scale
        # Schedule the update function to run after 100 milliseconds
        t = self.root.after(100, self.update_uniform_noise, low_scale, high_scale, frame)
        self.tid = t

    else:
        tk.messagebox.showinfo("Error", "No image loaded")


def update_uniform_noise(self, low_scale, high_scale, frame):
    addnoise = Addnoise()
    if self.using_transformations == self.uniform_noise:
        low = low_scale.get()
        high = high_scale.get()
        if high < low:
            tk.messagebox.showerror("Error", "Invalid change ,high counld not less than low")
            high = low
        if self.cache1 == low and self.cache2 == high:
            # Schedule the next update after 300 milliseconds
            t = self.root.after(300, self.update_uniform_noise, low_scale, high_scale, frame)
            self.tid = t
            return
        # Perform the mean filter operation
        self.processed_image = addnoise.uniform_noise(self.original_image, low, high)
        # Display the original and processed images
        self.compare_images(self.original_image, self.processed_image)
        # Schedule the next update after 100 milliseconds
        t = self.root.after(100, self.update_uniform_noise, low_scale, high_scale, frame)
        self.tid = t
        return
    else:
        # Remove the kernel size bar and buttons
        frame.destroy()
        return


def mod_window_before_sp_noise(self):
    if self.using_transformations != self.sp_noise:
        # Create a frame to hold the kernel size bar and buttons
        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP, pady=10)
        # Label and Scale for kernel size
        label = tk.Label(frame, text="Select mean:")
        label.pack(side=tk.LEFT, padx=10)
        amount_var = tk.DoubleVar()
        amount_scale = tk.Scale(frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL, variable=amount_var,
                                resolution=0.1)
        amount_scale.pack(side=tk.LEFT, padx=10)

    else:
        # find the frame that holds the kernel size bar and buttons
        # print(self.root.winfo_children())
        frame = self.root.winfo_children()[3]
        amount_scale = frame.winfo_children()[1]

    return amount_scale, frame


def sp_noise(self):
    if self.original_image:
        amount_scale, frame = self.mod_window_before_sp_noise()
        self.using_transformations = self.sp_noise
        self.cache1 = amount_scale
        # Schedule the update function to run after 100 milliseconds
        t = self.root.after(100, self.update_sp_noise, amount_scale, frame)
        self.tid = t
    else:
        tk.messagebox.showinfo("Error", "No image loaded")


def update_sp_noise(self, amount_scale, frame):
    addnoise = Addnoise()
    if self.using_transformations == self.sp_noise:
        amount = amount_scale.get()
        if self.cache1 == amount:
            # Schedule the next update after 300 milliseconds
            t = self.root.after(300, self.update_sp_noise, amount_scale, frame)
            self.tid = t
            return
        # Perform the mean filter operation
        self.processed_image = addnoise.sp_noise(self.original_image, amount)
        # Display the original and processed images
        self.compare_images(self.original_image, self.processed_image)
        # Schedule the next update after 100 milliseconds
        t = self.root.after(100, self.update_sp_noise, amount_scale, frame)
        self.tid = t
        return
    else:
        # Remove the kernel size bar and buttons
        frame.destroy()
        return


def mod_window_before_gamma_noise(self):
    if self.using_transformations != self.gamma_noise:
        # Create a frame to hold the kernel size bar and buttons
        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP, pady=10)
        # Label and Scale for kernel size
        label = tk.Label(frame, text="Select mean:")
        label.pack(side=tk.LEFT, padx=10)
        scale_var = tk.DoubleVar()
        scale_scale = tk.Scale(frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL, variable=scale_var,
                               resolution=0.1)
        scale_scale.pack(side=tk.LEFT, padx=10)

    else:
        # find the frame that holds the kernel size bar and buttons
        # print(self.root.winfo_children())
        frame = self.root.winfo_children()[3]
        scale_scale = frame.winfo_children()[1]

    return scale_scale, frame


def gamma_noise(self):
    if self.original_image:
        scale_scale, frame = self.mod_window_before_gamma_noise()
        self.using_transformations = self.gamma_noise
        self.cache1 = scale_scale
        # Schedule the update function to run after 100 milliseconds
        t = self.root.after(100, self.update_gamma_noise, scale_scale, frame)
        self.tid = t
    else:
        tk.messagebox.showinfo("Error", "No image loaded")


def update_gamma_noise(self, scale_scale, frame):
    addnoise = Addnoise()
    if self.using_transformations == self.gamma_noise:
        scale = scale_scale.get()
        if self.cache1 == scale:
            # Schedule the next update after 300 milliseconds
            t = self.root.after(300, self.update_gamma_noise, scale_scale, frame)
            self.tid = t
            return
        # Perform the mean filter operation
        self.processed_image = addnoise.gamma_noise(self.original_image, scale)
        # Display the original and processed images
        self.compare_images(self.original_image, self.processed_image)
        # Schedule the next update after 100 milliseconds
        t = self.root.after(100, self.update_gamma_noise, scale_scale, frame)
        self.tid = t
        return
    else:
        # Remove the kernel size bar and buttons
        frame.destroy()
        return


def mod_window_before_exp_noise(self):
    if self.using_transformations != self.exp_noise:
        # Create a frame to hold the kernel size bar and buttons
        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP, pady=10)
        # Label and Scale for kernel size
        label = tk.Label(frame, text="Select mean:")
        label.pack(side=tk.LEFT, padx=10)
        scale_var = tk.DoubleVar()
        scale_scale = tk.Scale(frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL, variable=scale_var,
                               resolution=0.1)
        scale_scale.pack(side=tk.LEFT, padx=10)

    else:
        # find the frame that holds the kernel size bar and buttons
        # print(self.root.winfo_children())
        frame = self.root.winfo_children()[3]
        scale_scale = frame.winfo_children()[1]

    return scale_scale, frame


def exp_noise(self):
    if self.original_image:
        scale_scale, frame = self.mod_window_before_exp_noise()
        self.using_transformations = self.exp_noise
        self.cache1 = scale_scale
        # Schedule the update function to run after 100 milliseconds
        t = self.root.after(100, self.update_exp_noise, scale_scale, frame)
        self.tid = t
    else:
        tk.messagebox.showinfo("Error", "No image loaded")


def update_exp_noise(self, scale_scale, frame):
    addnoise = Addnoise()
    if self.using_transformations == self.exp_noise:
        scale = scale_scale.get()
        if self.cache1 == scale:
            # Schedule the next update after 300 milliseconds
            t = self.root.after(300, self.update_exp_noise, scale_scale, frame)
            self.tid = t
            return
        # Perform the mean filter operation
        self.processed_image = addnoise.exponential_noise(self.original_image, scale)
        # Display the original and processed images
        self.compare_images(self.original_image, self.processed_image)
        # Schedule the next update after 100 milliseconds
        t = self.root.after(100, self.update_exp_noise, scale_scale, frame)
        self.tid = t
        return
    else:
        # Remove the kernel size bar and buttons
        frame.destroy()
        return


def mod_window_before_ray_noise(self):
    if self.using_transformations != self.ray_noise:
        # Create a frame to hold the kernel size bar and buttons
        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP, pady=10)
        # Label and Scale for kernel size
        label = tk.Label(frame, text="Select mean:")
        label.pack(side=tk.LEFT, padx=10)
        scale_var = tk.DoubleVar()
        scale_scale = tk.Scale(frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL, variable=scale_var,
                               resolution=0.1)
        scale_scale.pack(side=tk.LEFT, padx=10)

    else:
        # find the frame that holds the kernel size bar and buttons
        # print(self.root.winfo_children())
        frame = self.root.winfo_children()[3]
        scale_scale = frame.winfo_children()[1]

    return scale_scale, frame


def ray_noise(self):
    if self.original_image:
        scale_scale, frame = self.mod_window_before_ray_noise()
        self.using_transformations = self.ray_noise
        self.cache1 = scale_scale
        # Schedule the update function to run after 100 milliseconds
        t = self.root.after(100, self.update_ray_noise, scale_scale, frame)
        self.tid = t
    else:
        tk.messagebox.showinfo("Error", "No image loaded")


def update_ray_noise(self, scale_scale, frame):
    addnoise = Addnoise()
    if self.using_transformations == self.ray_noise:
        scale = scale_scale.get()
        if self.cache1 == scale:
            # Schedule the next update after 300 milliseconds
            t = self.root.after(300, self.update_ray_noise, scale_scale, frame)
            self.tid = t
            return
        # Perform the mean filter operation
        self.processed_image = addnoise.rayl_noise(self.original_image, scale)
        # Display the original and processed images
        self.compare_images(self.original_image, self.processed_image)
        # Schedule the next update after 100 milliseconds
        t = self.root.after(100, self.update_ray_noise, scale_scale, frame)
        self.tid = t
        return
    else:
        # Remove the kernel size bar and buttons
        frame.destroy()
        return