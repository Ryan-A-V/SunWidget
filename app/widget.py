from PyQt5 import QtWidgets, QtCore, QtGui
import json, os
from app.settings_dialog import SettingsDialog

CONFIG_FILE = "config.json"

class ImageWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnBottomHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.click_timer = QtCore.QElapsedTimer()
        self.load_config()
        self.setFixedSize(*self.config["widget_size"])
        self.setWindowOpacity(self.config["widget_opacity"])

        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        self.update_image()

    def load_config(self):
        with open(CONFIG_FILE, 'r') as f:
            self.config = json.load(f)

    def save_config(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get_current_image_list(self):
        shape = self.config.get("shape", "rectangle")
        return self.config.get("circle_images" if shape == "circle" else "square_images", [])

    def update_image(self):
        images = self.get_current_image_list()
        if not images:
            return
        path = images[self.config["image_index"] % len(images)]
        if not os.path.exists(path):
            return

        base_pixmap = QtGui.QPixmap(path).scaled(self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        # Composite with border
        composed = QtGui.QPixmap(self.size())
        composed.fill(QtCore.Qt.transparent)

        painter = QtGui.QPainter(composed)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.drawPixmap(
            (self.width() - base_pixmap.width()) // 2,
            (self.height() - base_pixmap.height()) // 2,
            base_pixmap
        )

        # Draw border on top
        pen = QtGui.QPen(QtGui.QColor(self.config["border_color"]))
        pen.setWidth(self.config["border_thickness"])
        painter.setPen(pen)

        if self.config["shape"] == "circle":
            painter.drawEllipse(self.rect().adjusted(2, 2, -2, -2))
        else:
            painter.drawRect(self.rect().adjusted(2, 2, -2, -2))

        painter.end()
        self.label.setPixmap(composed)


    def cycle_image(self):
        images = self.get_current_image_list()
        if not images:
            return
        self.config["image_index"] = (self.config["image_index"] + 1) % len(images)
        self.save_config()
        self.update_image()


    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen(QtGui.QColor(self.config["border_color"]))
        pen.setWidth(self.config["border_thickness"])
        pen.setColor(QtGui.QColor(self.config["border_color"]))
        painter.setPen(pen)
        if self.config["shape"] == "circle":
            painter.drawEllipse(self.rect().adjusted(2, 2, -2, -2))
        else:
            painter.drawRect(self.rect().adjusted(2, 2, -2, -2))

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.click_timer.start()
            self.drag_origin = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.drag_origin)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            elapsed = self.click_timer.elapsed()
            if elapsed < 300:
                self.cycle_image()
            else:
                self.shake()
        elif event.button() == QtCore.Qt.RightButton:
            dialog = SettingsDialog(self.config, self)
            if dialog.exec_():
                self.config = dialog.get_config()
                self.save_config()
                self.apply_settings()

    def apply_settings(self):
        self.setFixedSize(*self.config["widget_size"])
        self.setWindowOpacity(self.config["widget_opacity"])
        self.update_image()
        self.repaint()

    def shake(self):
        animation = QtCore.QPropertyAnimation(self, b"pos")
        animation.setDuration(300)
        animation.setLoopCount(2)
        current_pos = self.pos()
        animation.setKeyValueAt(0, current_pos)
        animation.setKeyValueAt(0.25, current_pos + QtCore.QPoint(-10, 0))
        animation.setKeyValueAt(0.5, current_pos + QtCore.QPoint(10, 0))
        animation.setKeyValueAt(0.75, current_pos + QtCore.QPoint(-10, 0))
        animation.setKeyValueAt(1, current_pos)
        animation.start(QtCore.QAbstractAnimation.DeleteWhenStopped)

def run_widget():
    app = QtWidgets.QApplication([])
    widget = ImageWidget()
    widget.show()
    app.exec_()
