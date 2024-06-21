import cv2
import numpy as np
import os


def select_image():
    """
    Выбор изображения для обработки.

    Returns:
    - numpy массив, представляющий выбранное изображение.
    """
    while True:
        print("Выберите источник изображения:")
        print("1. Сделать новое фото с веб-камеры")
        print("2. Загрузить изображение из папки images")
        choice = input("Введите номер (1 или 2): ")

        if choice == '1':
            image = capture_webcam()
            if image is not None:
                return image
        elif choice == '2':
            image = load_from_folder()
            if image is not None:
                return image
        else:
            print("Неверный ввод. Пожалуйста, выберите 1 или 2.")


def capture_webcam():
    """
    Захват изображения с веб-камеры.

    Returns:
    - numpy массив, представляющий захваченное изображение.
    """
    cap = cv2.VideoCapture(0)  # Захват с первой доступной камеры
    if not cap.isOpened():
        print("Не удалось подключиться к веб-камере.")
        return None

    ret, frame = cap.read()
    if not ret:
        print("Не удалось захватить кадр с веб-камеры.")
        return None

    cap.release()
    return frame


def load_from_folder():
    """
    Загрузка изображения из папки images.

    Returns:
    - numpy массив, представляющий загруженное изображение.
    """
    image_path = 'images/example.jpg'  # Укажите корректный путь к изображению
    if not os.path.exists(image_path):
        print(f"Изображение по пути {image_path} не найдено.")
        return None

    image = cv2.imread(image_path)
    if image is None:
        print(f"Не удалось загрузить изображение по пути: {image_path}")
    return image


def resize_image(image, width, height):
    """
    Изменение размера изображения.

    Args:
    - image: numpy массив, представляющий изображение.
    - width: новая ширина изображения.
    - height: новая высота изображения.

    Returns:
    - numpy массив, представляющий измененное изображение.
    """
    resized_image = cv2.resize(image, (width, height))
    return resized_image


def decrease_brightness(image, value):
    """
    Понижение яркости изображения.

    Args:
    - image: numpy массив, представляющий изображение.
    - value: значение для понижения яркости (0-100).

    Returns:
    - numpy массив, представляющий измененное изображение.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = np.where(v <= value, 0, v - value)
    final_hsv = cv2.merge((h, s, v))
    brightness_decreased_image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return brightness_decreased_image


def draw_red_circle(image, center_x, center_y, radius):
    """
    Нарисовать красный круг на изображении.

    Args:
    - image: numpy массив, представляющий изображение.
    - center_x: координата x центра круга.
    - center_y: координата y центра круга.
    - radius: радиус круга.

    Returns:
    - numpy массив, представляющий изображение с нарисованным кругом.
    """
    red_color = (0, 0, 255)  # BGR формат
    thickness = 2  # толщина круга
    cv2.circle(image, (center_x, center_y), radius, red_color, thickness)
    return image


def main_menu(image):
    """
    Главное меню приложения.

    Args:
    - image: numpy массив, представляющий изображение.
    """
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
        elif choice == '2':
            value = int(input("Введите значение для понижения яркости (0-100): "))
            image = decrease_brightness(image, value)
            cv2.imshow("Processed Image", image)
            cv2.waitKey(0)
        elif choice == '3':
            center_x = int(input("Введите координату x центра круга: "))
            center_y = int(input("Введите координату y центра круга: "))
            radius = int(input("Введите радиус круга: "))
            image = draw_red_circle(image, center_x, center_y, radius)
            cv2.imshow("Processed Image", image)
            cv2.waitKey(0)
        elif choice == '4':
            image = select_image()
            if image is None:
                continue
            cv2.imshow("Original Image", image)
            cv2.waitKey(0)
        elif choice == '5':
            break
        else:
            print("Неверный ввод. Пожалуйста, выберите действие от 1 до 5.")


def main():
    image = select_image()
    if image is not None:
        cv2.imshow("Original Image", image)
        cv2.waitKey(0)  # Ожидание нажатия клавиши без таймаута
        main_menu(image)


if __name__ == "__main__":
    main()
