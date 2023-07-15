import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import imghdr
import cv2
# Constants for styling
PRIMARY_COLOR = "#01162F"
FONT = ("Arial", 12)
# Load the image file and display it on the canvas
def load_image():
    global cv_img, img_h, img_w, img_c, img_format, original_cv_img
    file_path = filedialog.askopenfilename()
    if file_path:
        file_path = os.path.abspath(file_path)
        if not os.path.isfile(file_path):
            messagebox.showerror("Error", "File does not exist!")
            return
        img_format = imghdr.what(file_path)
        if not img_format:
            messagebox.showerror("Error", "Unsupported file format!")
            return
        cv_img = cv2.imread(file_path)
        if cv_img is not None:
            img_h, img_w, img_c = cv_img.shape
            original_cv_img = cv_img.copy()  # save a copy of the original image
            update_image()
        else:
            messagebox.showerror("Error", "Failed to load image!")

# Update the canvas with the current image
def update_image():
    global cv_img, img_h, img_w, img_c, img_format
    img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    canvas.create_image(canvas.winfo_width()//2, canvas.winfo_height()//2, anchor=tk.CENTER, image=img)
    canvas.image = img

# Reset the image to its original state
def reset_image():
    global cv_img, img_h, img_w, img_c, img_format, original_cv_img
    cv_img = original_cv_img.copy()
    update_image()

# Resize the image to a new width and height
def resize_image():
    global cv_img, img_h, img_w, img_c, img_format
    new_w = int(width_entry.get())
    new_h = int(height_entry.get())
    cv_img = cv2.resize(cv_img, (new_w, new_h))
    img_h, img_w = new_h, new_w
    update_image()

# Convert the image to grayscale
def grayscale_image():
    global cv_img, img_h, img_w, img_c, img_format
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    update_image()

# Apply a Gaussian blur to the image
def blur_image():
    global cv_img, img_h, img_w, img_c, img_format
    cv_img = cv2.GaussianBlur(cv_img, (3, 3), 0)
    update_image()

# Rotate the image by a given angle
def rotate_image():
    global cv_img, img_h, img_w, img_c, img_format
    angle = float(angle_entry.get())
    center = (img_w // 2, img_h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    cv_img = cv2.warpAffine(cv_img, rotation_matrix, (img_w, img_h))
    update_image()

# Adjust the color balance of the image
def adjust_color_balance():
    global cv_img, img_h, img_w, img_c, img_format
    red_scale = float(red_scale_entry.get())
    green_scale = float(green_scale_entry.get())
    blue_scale = float(blue_scale_entry.get())
    cv_img[:,:,0] = cv_img[:,:,0] * blue_scale
    cv_img[:,:,1] = cv_img[:,:,1] * green_scale
    cv_img[:,:,2] = cv_img[:,:,2] * red_scale
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    update_image()

# Save the current image to a file
def save_image():
    global cv_img, img_h, img_w, img_c, img_format
    file_path = filedialog.asksaveasfilename(defaultextension='.' + img_format)
    if file_path:
        cv2.imwrite(file_path, cv_img)

# Delete the current image
def delete_image():
    global cv_img, img_h, img_w, img_c, img_format, original_cv_img
    canvas.delete("all")
    cv_img = None
    img_h, img_w, img_c = 0, 0, 0
    img_format = None
    original_cv_img = None
# Create the main window
root = tk.Tk()
root.title("The World of Image Processing by Amjad Ahmad")
root.geometry("800x600")
root.configure(background="#F5FBFF")

# Create a canvas to display the image #F1F3F6
canvas = tk.Canvas(root, width=600, height=400, bg="#F9FCFF")
canvas.pack(padx=20, pady=20)

# Create frames for the buttons
button_frame_1 = tk.Frame(root)
button_frame_1.pack(side=tk.TOP, padx=15, pady=15)

button_frame_2 = tk.Frame(root)
button_frame_2.pack(side=tk.TOP, padx=15, pady=15)

button_frame_3 = tk.Frame(root)
button_frame_3.pack(side=tk.TOP, padx=15, pady=15)

# Create buttons for loading and resetting the image
# Create buttons for loading and resetting the image
load_button = tk.Button(button_frame_1, text="Load Image", bg=PRIMARY_COLOR, fg="white", font=FONT, command=load_image)
load_button.pack(side=tk.LEFT, padx=10)

reset_button = tk.Button(button_frame_1, text="Reset Image", bg=PRIMARY_COLOR, fg="white", font=FONT, command=reset_image)
reset_button.pack(side=tk.LEFT, padx=10)

delete_button = tk.Button(button_frame_1, text="Delete Image", bg=PRIMARY_COLOR, fg="white", font=FONT, command=delete_image)
delete_button.pack(side=tk.LEFT, padx=10)
blur_button = tk.Button(button_frame_1, text="Blur", bg=PRIMARY_COLOR, fg="white", font=FONT, command=blur_image)
blur_button.pack(side=tk.LEFT, padx=10)
# Create buttons for grayscale and blur filters
grayscale_button = tk.Button(button_frame_1, text="Grayscale", bg=PRIMARY_COLOR, fg="white", font=FONT, command=grayscale_image)
grayscale_button.pack(side=tk.LEFT, padx=10)

# Create buttons for rotating and saving the 

# Create buttons for resizing the image
width_label = tk.Label(button_frame_2, text="Width:", font=FONT)
width_label.pack(side=tk.LEFT, padx=10)

width_entry = tk.Entry(button_frame_2, font=FONT, width=5)
width_entry.pack(side=tk.LEFT)

height_label = tk.Label(button_frame_2, text="Height:", font=FONT)
height_label.pack(side=tk.LEFT, padx=10)

height_entry = tk.Entry(button_frame_2, font=FONT, width=5)
height_entry.pack(side=tk.LEFT)

resize_button = tk.Button(button_frame_2, text="Resize", bg=PRIMARY_COLOR, fg="white", font=FONT, command=resize_image)
resize_button.pack(side=tk.LEFT, padx=10)

angle_label = tk.Label(button_frame_2, text="Angle:", font=FONT)
angle_label.pack(side=tk.LEFT, padx=10)

angle_entry = tk.Entry(button_frame_2, font=FONT, width=5)
angle_entry.pack(side=tk.LEFT)

rotate_button = tk.Button(button_frame_2, text="Rotate", bg=PRIMARY_COLOR, fg="white", font=FONT, command=rotate_image)
rotate_button.pack(side=tk.LEFT, padx=10)

save_button = tk.Button(button_frame_2, text="Save Image", bg=PRIMARY_COLOR, fg="white", font=FONT, command=save_image)
save_button.pack(side=tk.LEFT, padx=10)
# Create buttons for adjusting the color balance
red_scale_label = tk.Label(button_frame_3, text="Red Scale:", font=FONT)
red_scale_label.pack(side=tk.LEFT, padx=10)

red_scale_entry = tk.Entry(button_frame_3, font=FONT, width=5)
red_scale_entry.pack(side=tk.LEFT)

green_scale_label = tk.Label(button_frame_3, text="Green Scale:", font=FONT)
green_scale_label.pack(side=tk.LEFT, padx=10)

green_scale_entry = tk.Entry(button_frame_3, font=FONT, width=5)
green_scale_entry.pack(side=tk.LEFT)

blue_scale_label = tk.Label(button_frame_3, text="Blue Scale:", font=FONT)
blue_scale_label.pack(side=tk.LEFT, padx=10)

blue_scale_entry = tk.Entry(button_frame_3, font=FONT, width=5)
blue_scale_entry.pack(side=tk.LEFT)

color_balance_button = tk.Button(button_frame_3, text="Adjust Color Balance", bg=PRIMARY_COLOR, fg="white", font=FONT, command=adjust_color_balance)
color_balance_button.pack(side=tk.LEFT, padx=10)
# Run the main loop
root.mainloop()