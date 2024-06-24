import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, \
    QWidget, QInputDialog, QDialog
from PyQt5.QtGui import QImage, QPixmap, QPalette, QColor
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

        self.setStyleSheet("color: black; font: 16px Arial;")
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
        self.edit_window = EditWindow(image, self)
        self.edit_window.show()


class EditWindow(QDialog):
    def __init__(self, image, parent=None):
        super().__init__(parent)
        self.image = image
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Редактирование изображения")
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(800, 600)  # Запрет на изменение размера окна

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

        layout.addLayout(button_layout)

        self.setStyleSheet("color: black; font: 16px Arial;")
        resize_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 15px; padding: 10px;")
        brightness_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 15px; padding: 10px;")
        circle_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 15px; padding: 10px;")
        save_button.setStyleSheet("background-color: #2196F3; color: white; border-radius: 15px; padding: 10px;")
        close_button.setStyleSheet("background-color: #f44336; color: white; border-radius: 15px; padding: 10px;")

    def update_image(self, image):
        qimage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)

    def resize_image_dialog(self):
        width, ok = QInputDialog.getInt(self, "Изменить размер", "Введите ширину:")
        if ok:
            height, ok = QInputDialog.getInt(self, "Изменить размер", "Введите высоту:")
            if ok:
                self.image = self.resize_image(self.image, width, height)
                self.update_image(self.image)

    def decrease_brightness_dialog(self):
        value, ok = QInputDialog.getInt(self, "Понизить яркость", "Введите значение уменьшения яркости:")
        if ok:
            self.image = self.decrease_brightness(self.image, value)
            self.update_image(self.image)

    def draw_circle_dialog(self):
        x, ok = QInputDialog.getInt(self, "Нарисовать круг", "Введите координату x:")
        if ok:
            y, ok = QInputDialog.getInt(self, "Нарисовать круг", "Введите координату y:")
            if ok:
                radius, ok = QInputDialog.getInt(self, "Нарисовать круг", "Введите радиус:")
                if ok:
                    self.image = self.draw_circle(self.image, (x, y), radius)
                    self.update_image(self.image)

    def resize_image(self, image, width, height):
        return cv2.resize(image, (width, height))

    def decrease_brightness(self, image, value):
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        h, s, v = cv2.split(hsv)
        v = cv2.subtract(v, value)
        final_hsv = cv2.merge((h, s, v))
        return cv2.cvtColor(final_hsv, cv2.COLOR_HSV2RGB)

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

            # Опционально: можно добавить сообщение об успешном сохранении
            # QMessageBox.information(self, "Изображение сохранено", f"Изображение сохранено как {file_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessingApp()
    window.show()
    sys.exit(app.exec_())
