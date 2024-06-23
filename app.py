import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget, \
    QInputDialog, QDialog
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer


class ImageProcessingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приложение для обработки изображений")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #d7ffb9;")  # Зеленый цвет для фона

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 2px solid #4CAF50; background-color: #f0f0f0;")
        self.image_label.setGeometry(50, 50, 600, 400)

        self.initUI()

        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.is_camera_active = False  # Флаг для состояния трансляции с камеры

    def initUI(self):
        self.camera_button = QPushButton("Трансляция камеры", self)
        self.camera_button.clicked.connect(self.toggle_camera)
        self.camera_button.setGeometry(50, 480, 200, 50)

        load_button = QPushButton("Загрузить изображение", self)
        load_button.clicked.connect(self.load_image)
        load_button.setGeometry(300, 480, 200, 50)

        resize_button = QPushButton("Изменить размер", self)
        resize_button.clicked.connect(self.resize_image)
        resize_button.setGeometry(550, 480, 200, 50)

        brightness_button = QPushButton("Уменьшить яркость", self)
        brightness_button.clicked.connect(self.decrease_brightness)
        brightness_button.setGeometry(50, 540, 200, 50)

        circle_button = QPushButton("Нарисовать круг", self)
        circle_button.clicked.connect(self.draw_circle)
        circle_button.setGeometry(300, 540, 200, 50)

        exit_button = QPushButton("Выход", self)
        exit_button.clicked.connect(self.close)
        exit_button.setGeometry(550, 540, 200, 50)

        self.setStyleSheet("color: black; font: 14px Arial;")
        self.camera_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px;")
        load_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px;")
        resize_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px;")
        brightness_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px;")
        circle_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px;")
        exit_button.setStyleSheet("background-color: #f44336; color: white; border-radius: 10px;")

    def toggle_camera(self):
        if not self.is_camera_active:
            self.camera_button.setText("Скриншот")
            self.timer.start(1000 // 30)  # 30 FPS
            self.is_camera_active = True
        else:
            self.camera_button.setText("Трансляция камеры")
            self.timer.stop()
            self.is_camera_active = False

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.show_error("Не удалось захватить изображение с вебкамеры.")
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Конвертируем изображение в RGB
        self.image = frame_rgb
        self.display_image(self.image)

    def load_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Открыть изображение", "", "Изображения (*.jpg *.jpeg *.png)",
                                                   options=options)
        if file_name:
            self.timer.stop()  # Останавливаем захват с вебкамеры, если он запущен
            self.image = cv2.imread(file_name)
            if self.image is None:
                self.show_error("Не удалось загрузить изображение.")
                return
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)  # Конвертируем изображение в RGB
            self.display_image(self.image)

    def resize_image(self):
        if not hasattr(self, 'image'):
            self.show_error("Изображение не загружено.")
            return

        width, ok = QInputDialog.getInt(self, "Изменить размер изображения", "Введите новую ширину:")
        if not ok:
            return
        height, ok = QInputDialog.getInt(self, "Изменить размер изображения", "Введите новую высоту:")
        if not ok:
            return

        self.image = cv2.resize(self.image, (width, height))
        self.display_image(self.image)

    def decrease_brightness(self):
        if not hasattr(self, 'image'):
            self.show_error("Изображение не загружено.")
            return

        value, ok = QInputDialog.getInt(self, "Уменьшить яркость изображения", "Введите значение яркости (0-100):", 0,
                                        0, 100)
        if not ok:
            return

        hsv = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV)
        h, s, v = cv2.split(hsv)
        v = np.where(v <= value, 0, v - value)
        final_hsv = cv2.merge((h, s, v))
        self.image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2RGB)
        self.display_image(self.image)

    def draw_circle(self):
        if not hasattr(self, 'image'):
            self.show_error("Изображение не загружено.")
            return

        center_x, ok = QInputDialog.getInt(self, "Нарисовать круг на изображении", "Введите X координату центра круга:")
        if not ok:
            return
        center_y, ok = QInputDialog.getInt(self, "Нарисовать круг на изображении", "Введите Y координату центра круга:")
        if not ok:
            return
        radius, ok = QInputDialog.getInt(self, "Нарисовать круг на изображении", "Введите радиус круга:")
        if not ok:
            return

        red_color = (255, 0, 0)
        thickness = 2
        cv2.circle(self.image, (center_x, center_y), radius, red_color, thickness)
        self.display_image(self.image)

    def display_image(self, image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

    def show_error(self, message):
        error_dialog = QDialog(self)
        error_dialog.setWindowTitle("Ошибка")
        error_dialog.setGeometry(200, 200, 400, 200)
        error_label = QLabel(message, error_dialog)
        error_label.setStyleSheet("color: red;")
        error_label.setAlignment(Qt.AlignCenter)
        error_layout = QVBoxLayout()
        error_layout.addWidget(error_label)
        error_dialog.setLayout(error_layout)
        error_dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ImageProcessingApp()
    main_window.show()
    sys.exit(app.exec_())
