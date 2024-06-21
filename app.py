import cv2
import numpy as np
from matplotlib import pyplot as plt
from tkinter import filedialog
from tkinter import Tk


def load_image():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    if file_path:
        image = cv2.imread(file_path)
        return image
    return None


def show_image(image):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()


def show_channel(image, channel):
    channel_map = {'r': 2, 'g': 1, 'b': 0}
    channel_img = np.zeros_like(image)
    channel_img[:, :, channel_map[channel]] = image[:, :, channel_map[channel]]
    show_image(channel_img)


def capture_image_from_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return None
    ret, frame = cap.read()
    cap.release()
    if ret:
        return frame
    else:
        print("Error: Could not capture image.")
        return None


if __name__ == "__main__":
    print("Choose an option:")
    print("1. Load an image")
    print("2. Capture image from webcam")
    choice = input("Enter choice: ")

    if choice == '1':
        img = load_image()
    elif choice == '2':
        img = capture_image_from_webcam()
    else:
        print("Invalid choice.")
        img = None

    if img is not None:
        show_image(img)
        print("Choose a channel to display (r, g, b):")
        channel = input("Enter channel: ")
        if channel in ['r', 'g', 'b']:
            show_channel(img, channel)
        else:
            print("Invalid channel.")
