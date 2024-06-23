import cv2
import numpy as np
import os
from tkinter import Tk, filedialog


def select_image():
    while True:
        print("Выберите источник изображения:")
        print("1. Сделать новое фото с веб-камеры")
        print("2. Выбрать файл изображения через обозреватель")
        choice = input("Введите номер (1 или 2): ")

        if choice == '1':
            image = capture_webcam()
            if image is not None:
                return image
        elif choice == '2':
            image = load_from_file_dialog()
            if image is not None:
                return image
        else:
            print("Неверный ввод. Пожалуйста, выберите 1 или 2.")


def capture_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Не удалось подключиться к веб-камере.")
        return None

    ret, frame = cap.read()
    cap.release()
    if not ret:
        print("Не удалось захватить кадр с веб-камеры.")
        return None
    return frame


def load_from_file_dialog():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(
        title="Выберите файл изображения",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )
    root.destroy()
    if not file_path:
        print("Файл не выбран.")
        return None

    print(f"Выбран файл: {file_path}")
    image = cv2.imread(file_path)
    if image is None:
        print(f"Не удалось загрузить изображение по пути: {file_path}")
    return image


def resize_image(image, width, height):
    return cv2.resize(image, (width, height))


def decrease_brightness(image, value):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = np.where(v <= value, 0, v - value)
    final_hsv = cv2.merge((h, s, v))
    return cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)


def draw_red_circle(image, center_x, center_y, radius):
    red_color = (0, 0, 255)
    thickness = 2
    cv2.circle(image, (center_x, center_y), radius, red_color, thickness)
    return image


def main_menu(image):
    while True:
        print("\nГлавное меню:")
        print("1. Изменить размер изображения")
        print("2. Понизить яркость изображения")
        print("3. Нарисовать красный круг")
        print("4. Выбрать новое изображение")
        print("5. Выйти из программы")

        choice = input("Выберите действие (1-5): ")

        if choice == '1':
            width = int(input("Введите новую ширину изображения: "))
            height = int(input("Введите новую высоту изображения: "))
            image = resize_image(image, width, height)
            cv2.imshow("Processed Image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        elif choice == '2':
            value = int(input("Введите значение для понижения яркости (0-100): "))
            image = decrease_brightness(image, value)
            cv2.imshow("Processed Image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        elif choice == '3':
            center_x = int(input("Введите координату x центра круга: "))
            center_y = int(input("Введите координату y центра круга: "))
            radius = int(input("Введите радиус круга: "))
            image = draw_red_circle(image, center_x, center_y, radius)
            cv2.imshow("Processed Image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        elif choice == '4':
            image = select_image()
            if image is None:
                continue
            cv2.imshow("Original Image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        elif choice == '5':
            break
        else:
            print("Неверный ввод. Пожалуйста, выберите действие от 1 до 5.")


def main():
    image = select_image()
    if image is not None:
        cv2.imshow("Original Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        main_menu(image)


if __name__ == "__main__":
    main()
