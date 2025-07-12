from PyQt5 import QtWidgets, QtGui, QtCore
import os

class ImageSelectorDialog(QtWidgets.QDialog):
    def __init__(self, image_dir, selected_images, shape="rectangle", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Images")
        self.resize(400, 500)
        self.selected_images = selected_images
        self.image_dir = image_dir
        self.shape = shape
        self.checkboxes = []

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        inner = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(inner)

        suffix = "_square.png" if shape == "rectangle" else "_circle.png"

        for file in os.listdir(image_dir):
            if file.endswith(suffix):
                full_path = os.path.join(image_dir, file)
                row = QtWidgets.QHBoxLayout()
                cb = QtWidgets.QCheckBox(file)
                cb.setChecked(full_path in selected_images)
                row.addWidget(cb)

                preview = QtWidgets.QLabel()
                pixmap = QtGui.QPixmap(full_path)
                pixmap = pixmap.scaled(50, 50, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                preview.setPixmap(pixmap)
                row.addWidget(preview)

                layout.addLayout(row)
                self.checkboxes.append((cb, full_path))

        scroll.setWidget(inner)
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(scroll)

        apply_btn = QtWidgets.QPushButton("Apply")
        apply_btn.clicked.connect(self.accept)
        main_layout.addWidget(apply_btn)

        self.setLayout(main_layout)

    def get_selected(self):
        square_images = [path for cb, path in self.checkboxes if cb.isChecked()]
        circle_images = []

        for square_path in square_images:
            circle_path = square_path.replace("_square.png", "_circle.png")
            if os.path.exists(circle_path):
                circle_images.append(circle_path)
            else:
                print("Warning: Missing circle version for", square_path)

        return square_images, circle_images