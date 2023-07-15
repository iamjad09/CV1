import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
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


# Create the canvas for displaying the image
canvas = tk.Canvas(root, width=600, height=400, bg="#FFFFFF")
canvas.pack(side=tk.LEFT, padx=20, pady=20)

# Create the frame for the buttons
button_frame = tk.Frame(root, bg="#F5FBFF")
button_frame.pack(side=tk.RIGHT, padx=20)
icon1 = Image.open("upload.png")
icon1 = icon1.resize((40, 40))
icon1 = ImageTk.PhotoImage(icon1)
# Create the buttons
load_button = tk.Button(button_frame, text="Load Image", font=FONT, bg=PRIMARY_COLOR,image=icon1, fg="#FFFFFF", command=load_image)
load_button.pack(pady=10, padx=10, fill=tk.X)
#reset image
icon2 = Image.open("reset.png")
icon2 = icon2.resize((40, 40))
icon2 = ImageTk.PhotoImage(icon2)
reset_button = tk.Button(button_frame, text="Reset Image", font=FONT,image=icon2, bg=PRIMARY_COLOR, fg="#FFFFFF", command=reset_image)
reset_button.pack(pady=10, padx=10, fill=tk.X)

icon3 = Image.open("resize.png")
icon3 = icon3.resize((40, 40))
icon3 = ImageTk.PhotoImage(icon3)
resize_button = tk.Button(button_frame, text="Resize Image",image=icon3,font=FONT, bg=PRIMARY_COLOR, fg="#FFFFFF", command=lambda: resize_window.deiconify())
resize_button.pack(pady=10, padx=10, fill=tk.X)

icon4= Image.open("colors.png")
icon4= icon4.resize((40, 40))
icon4= ImageTk.PhotoImage(icon4)
grayscale_button = tk.Button(button_frame, text="Grayscale Image",image=icon4, font=FONT, bg=PRIMARY_COLOR, fg="#FFFFFF", command=grayscale_image)
grayscale_button.pack(pady=10, padx=10, fill=tk.X)

#blur image
icon5= Image.open("blur.png")
icon5= icon5.resize((40, 40))
icon5= ImageTk.PhotoImage(icon5)
blur_button = tk.Button(button_frame, text="Blur Image", image=icon5,font=FONT, bg=PRIMARY_COLOR, fg="#FFFFFF", command=blur_image)
blur_button.pack(pady=10, padx=10, fill=tk.X)

icon6= Image.open("360.png")
icon6= icon6.resize((40, 40))
icon6= ImageTk.PhotoImage(icon6)
rotate_button = tk.Button(button_frame, text="Rotate Image",image=icon6 ,font=FONT, bg=PRIMARY_COLOR, fg="#FFFFFF", command=lambda: rotate_window.deiconify())
rotate_button.pack(pady=10, padx=10, fill=tk.X)

icon7= Image.open("color-adjustment.png")
icon7= icon7.resize((40, 40))
icon7= ImageTk.PhotoImage(icon7)
color_balance_button = tk.Button(button_frame, text="Adjust Color Balance", image=icon7,font=FONT, bg=PRIMARY_COLOR, fg="#FFFFFF", command=lambda: color_balance_window.deiconify())
color_balance_button.pack(pady=10, padx=10, fill=tk.X)


icon8= Image.open("downloads.png")
icon8= icon8.resize((40, 40))
icon8= ImageTk.PhotoImage(icon8)
save_button = tk.Button(button_frame, text="Save Image", font=FONT,image=icon8, bg=PRIMARY_COLOR, fg="#FFFFFF", command=save_image)
save_button.pack(pady=10, padx=10, fill=tk.X)


# Create the window for resizing the image
icon9= Image.open("x.png")
icon9= icon9.resize((40, 40))
icon9= ImageTk.PhotoImage(icon9)
delete_button = tk.Button(button_frame, text="delete Image",image=icon9, font=FONT, bg=PRIMARY_COLOR, fg="#FFFFFF", command=delete_image)
delete_button.pack(pady=10, padx=10, fill=tk.X)

icon10= Image.open("resize.png")
icon10= icon10.resize((40, 40))
icon10= ImageTk.PhotoImage(icon10)
delete_button = tk.Button(button_frame, text="resize Image",image=icon10, font=FONT, bg=PRIMARY_COLOR, fg="#FFFFFF", command=resize_image)
resize_window = Toplevel(root)
resize_window.title("Resize Image")
resize_window.geometry("400x400")
resize_window.configure(background="#F5FBFF")
resize_window.withdraw()
width_label = tk.Label(resize_window, text="Width:", font=FONT, bg="#F5FBFF")
width_label.pack(pady=10)
width_entry = tk.Entry(resize_window, font=FONT)
width_entry.pack(padx=10, pady=10)
height_label = tk.Label(resize_window, text="Height:", font=FONT, bg="#F5FBFF")
height_label.pack(pady=10)

height_entry = tk.Entry(resize_window, font=FONT)
height_entry.pack(padx=10, pady=10)

resize_confirm_button = tk.Button(resize_window, text="Resize", font=FONT,image=icon9 ,bg=PRIMARY_COLOR, fg="#FFFFFF", command=resize_image)
resize_confirm_button.pack(pady=10, padx=10, fill=tk.X)

# Create the window for rotating the image
icon11= Image.open("360.png")
icon11= icon11.resize((40, 40))
icon11= ImageTk.PhotoImage(icon11)
rotate_window = Toplevel(root)
rotate_window.title("Rotate Image")
rotate_window.geometry("300x200")
rotate_window.configure(background="#F5FBFF")
rotate_window.withdraw()
angle_label = tk.Label(rotate_window, text="Angle (degrees):", font=FONT, bg="#F5FBFF")
angle_label.pack(pady=10)
angle_entry = tk.Entry(rotate_window, font=FONT)
angle_entry.pack(padx=10, pady=10)
rotate_confirm_button = tk.Button(rotate_window, text="Rotate",image=icon11,font=FONT, bg=PRIMARY_COLOR, fg="#FFFFFF", command=rotate_image)
rotate_confirm_button.pack(pady=10, padx=10, fill=tk.X)

# Create the window for adjusting color balance
color_balance_window = Toplevel(root)
color_balance_window.title("Adjust Color Balance")
color_balance_window.geometry("400x400")
color_balance_window.configure(background="#F5FBFF")
color_balance_window.withdraw()

icon12= Image.open("color-adjustment.png")
icon12= icon12.resize((40, 40))
icon12= ImageTk.PhotoImage(icon12)
red_scale_label = tk.Label(color_balance_window, text="Red Scale:", font=FONT, bg="#F5FBFF")
red_scale_label.pack(pady=10)

red_scale_entry = tk.Entry(color_balance_window, font=FONT)
red_scale_entry.pack(padx=10,pady=10)

green_scale_label = tk.Label(color_balance_window, text="Green Scale:", font=FONT, bg="#F5FBFF")
green_scale_label.pack(pady=10)

green_scale_entry = tk.Entry(color_balance_window, font=FONT)
green_scale_entry.pack(padx=10, pady=10)

blue_scale_label = tk.Label(color_balance_window, text="Blue Scale:", font=FONT, bg="#F5FBFF")
blue_scale_label.pack(pady=10)

blue_scale_entry = tk.Entry(color_balance_window, font=FONT)
blue_scale_entry.pack(padx=10, pady=10)

color_balance_confirm_button = tk.Button(color_balance_window, text="Adjust",image=icon12, font=FONT, bg=PRIMARY_COLOR, fg="#FFFFFF", command=adjust_color_balance)
color_balance_confirm_button.pack(pady=10, padx=10, fill=tk.X)

root.mainloop()