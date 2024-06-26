import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, \
    QWidget, QInputDialog, QDialog, QGroupBox, QRadioButton, QMessageBox
from PyQt5.QtGui import QImage, QPixmap, QPalette, QColor, QFont
from PyQt5.QtCore import Qt, QTimer, QSize


class ImageProcessingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приложение для обработки изображений")
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(800, 600)  # Запрет на изменение размера окна

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('#d7ffb9'))
        self.setPalette(palette)

        self.init_main_menu()

    def init_main_menu(self):
        self.main_menu_widget = QWidget(self)
        self.setCentralWidget(self.main_menu_widget)

        layout = QVBoxLayout(self.main_menu_widget)

        self.image_label = QLabel(self.main_menu_widget)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        button_layout = QVBoxLayout()

        self.camera_button = QPushButton("Трансляция камеры", self.main_menu_widget)
        self.camera_button.clicked.connect(self.toggle_camera)
        button_layout.addWidget(self.camera_button)

        load_button = QPushButton("Загрузить изображение", self.main_menu_widget)
        load_button.clicked.connect(self.load_image)
        button_layout.addWidget(load_button)

        exit_button = QPushButton("Выход", self.main_menu_widget)
        exit_button.clicked.connect(self.close)
        button_layout.addWidget(exit_button)

        layout.addLayout(button_layout)

        # Установка стиля и размера шрифта для кнопок
        font = QFont("Helvetica Neue", 16, QFont.Bold)  # Пример использования шрифта Helvetica Neue
        self.camera_button.setFont(font)
        load_button.setFont(font)
        exit_button.setFont(font)

        self.setStyleSheet("color: black;")

        self.camera_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 15px; padding: 10px;")
        load_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 15px; padding: 10px;")
        exit_button.setStyleSheet("background-color: #f44336; color: white; border-radius: 15px; padding: 10px;")

        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.is_camera_active = False

    def toggle_camera(self):
        if not self.is_camera_active:
            self.camera_button.setText("Скриншот")
            self.timer.start(1000 // 30)
            self.is_camera_active = True
        else:
            self.camera_button.setText("Трансляция камеры")
            self.timer.stop()
            self.is_camera_active = False
            self.open_edit_window(self.image)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.show_error("Не удалось захватить изображение с вебкамеры.")
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio)
        self.image_label.setPixmap(QPixmap.fromImage(p))
        self.image = frame_rgb

    def load_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Загрузить изображение", "", "Images (*.png *.xpm *.jpg)",
                                                   options=options)
        if file_name:
            self.image = cv2.imread(file_name)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.open_edit_window(self.image)

    def show_error(self, message):
        error_dialog = QDialog(self)
        error_dialog.setWindowTitle("Ошибка")
        error_dialog.setFixedSize(300, 100)
        layout = QVBoxLayout()
        label = QLabel(message, error_dialog)
        layout.addWidget(label)
        button = QPushButton("ОК", error_dialog)
        button.clicked.connect(error_dialog.accept)
        layout.addWidget(button)
        error_dialog.setLayout(layout)
        error_dialog.exec_()

    def open_edit_window(self, image):
        self.edit_window = EditWindow(image)
        self.edit_window.show()


class EditWindow(QDialog):
    def __init__(self, image, parent=None):
        super().__init__(parent)
        self.image = image
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Редактирование изображения")
        self.setGeometry(100, 100, 1000, 800)
        self.setFixedSize(1000, 800)  # Запрет на изменение размера окна

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('#d7ffb9'))
        self.setPalette(palette)

        layout = QVBoxLayout(self)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.update_image(self.image)
        layout.addWidget(self.image_label)

        button_layout = QVBoxLayout()

        resize_button = QPushButton("Изменить размер", self)
        resize_button.clicked.connect(self.resize_image_dialog)
        button_layout.addWidget(resize_button)

        brightness_button = QPushButton("Понизить яркость", self)
        brightness_button.clicked.connect(self.decrease_brightness_dialog)
        button_layout.addWidget(brightness_button)

        circle_button = QPushButton("Нарисовать круг", self)
        circle_button.clicked.connect(self.draw_circle_dialog)
        button_layout.addWidget(circle_button)

        save_button = QPushButton("Сохранить", self)
        save_button.clicked.connect(self.save_image)
        button_layout.addWidget(save_button)

        close_button = QPushButton("Закрыть", self)
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)

        # Уменьшили размер кнопок
        font = QFont("Helvetica Neue", 14, QFont.Bold)
        for btn in [resize_button, brightness_button, circle_button, save_button, close_button]:
            btn.setFont(font)
            btn.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 8px; padding: 6px;")

        layout.addLayout(button_layout)

        # Группа радиокнопок для выбора канала в одной линии
        self.channel_group = QGroupBox("Выбор канала", self)
        self.channel_layout = QHBoxLayout()

        self.red_channel_button = QRadioButton("Красный канал")
        self.green_channel_button = QRadioButton("Зелёный канал")
        self.blue_channel_button = QRadioButton("Синий канал")

        self.red_channel_button.setChecked(True)

        self.channel_layout.addWidget(self.red_channel_button)
        self.channel_layout.addWidget(self.green_channel_button)
        self.channel_layout.addWidget(self.blue_channel_button)

        self.channel_group.setLayout(self.channel_layout)
        layout.addWidget(self.channel_group)

        # Связываем кнопки с обработчиками
        self.red_channel_button.toggled.connect(lambda: self.update_image_channel("red"))
        self.green_channel_button.toggled.connect(lambda: self.update_image_channel("green"))
        self.blue_channel_button.toggled.connect(lambda: self.update_image_channel("blue"))

        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint)

    def update_image_channel(self, channel):
        if channel == "red":
            channel_idx = 0
        elif channel == "green":
            channel_idx = 1
        elif channel == "blue":
            channel_idx = 2
        else:
            return

        channel_image = self.image.copy()
        channel_image[:, :, (channel_idx + 1) % 3] = 0
        channel_image[:, :, (channel_idx + 2) % 3] = 0

        self.update_image(channel_image)

    def update_image(self, image):
        qimage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)

    def resize_image_dialog(self):
        width, ok = QInputDialog.getInt(self, "Изменить размер", "Введите ширину(1-800):", 800, 1, 800, 1)
        if ok:
            height, ok = QInputDialog.getInt(self, "Изменить размер", "Введите высоту(1-600):", 600, 1, 600, 1)
            if ok:
                self.image = self.resize_image(self.image, width, height)
                self.update_image(self.image)

    def decrease_brightness_dialog(self):
        value, ok = QInputDialog.getInt(self, "Понизить яркость", "Введите значение уменьшения яркости(1-255):", 50, 1, 255, 1)
        if ok:
            self.image = self.decrease_brightness(self.image, value)
            self.update_image(self.image)

    def draw_circle_dialog(self):
        x, ok = QInputDialog.getInt(self, "Нарисовать круг", "Введите координату x:", 0, -10000, 10000, 1)
        if ok:
            y, ok = QInputDialog.getInt(self, "Нарисовать круг", "Введите координату y:", 0, -10000, 10000, 1)
            if ok:
                radius, ok = QInputDialog.getInt(self, "Нарисовать круг", "Введите радиус:", 50, 1, 1000, 1)
                if ok:
                    self.image = self.draw_circle(self.image, (x, y), radius)
                    self.update_image(self.image)

    def resize_image(self, image, width, height):
        try:
            return cv2.resize(image, (width, height))
        except cv2.error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка изменения размера изображения: {str(e)}")

    def decrease_brightness(self, image, value):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = cv2.subtract(v, value)
        final_hsv = cv2.merge((h, s, v))
        return cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    def draw_circle(self, image, center, radius):
        return cv2.circle(image.copy(), center, radius, (0, 0, 255), 2)

    def save_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Сохранить изображение")
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")

        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            cv2.imwrite(file_path, cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessingApp()
    window.show()
    sys.exit(app.exec_())
