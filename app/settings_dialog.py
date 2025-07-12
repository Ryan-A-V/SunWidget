from PyQt5 import QtWidgets, QtCore
import json
import os

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.config = config.copy()
        self.setModal(True)
        layout = QtWidgets.QVBoxLayout()

        # Opacity slider
        self.opacity_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(int(self.config["widget_opacity"] * 100))
        layout.addWidget(QtWidgets.QLabel("Widget Opacity"))
        layout.addWidget(self.opacity_slider)

        # Width/Height
        self.width_box = QtWidgets.QSpinBox()
        self.height_box = QtWidgets.QSpinBox()
        self.width_box.setRange(50, 1000)
        self.height_box.setRange(50, 1000)
        self.width_box.setValue(self.config["widget_size"][0])
        self.height_box.setValue(self.config["widget_size"][1])
        layout.addWidget(QtWidgets.QLabel("Width"))
        layout.addWidget(self.width_box)
        layout.addWidget(QtWidgets.QLabel("Height"))
        layout.addWidget(self.height_box)

        # Shape selector
        self.shape_combo = QtWidgets.QComboBox()
        self.shape_combo.addItems(["rectangle", "circle"])
        self.shape_combo.setCurrentText(self.config["shape"])
        layout.addWidget(QtWidgets.QLabel("Shape"))
        layout.addWidget(self.shape_combo)

        # Border thickness
        self.border_thickness = QtWidgets.QSpinBox()
        self.border_thickness.setRange(0, 20)
        self.border_thickness.setValue(self.config["border_thickness"])
        layout.addWidget(QtWidgets.QLabel("Border Thickness"))
        layout.addWidget(self.border_thickness)
        
        # Border color
        self.color_button = QtWidgets.QPushButton("Choose Border Color")
        self.color_button.clicked.connect(self.select_color)
        layout.addWidget(self.color_button)
        
        # Image selection
        img_btn = QtWidgets.QPushButton("Select Images...")
        img_btn.clicked.connect(self.open_image_selector)
        layout.addWidget(img_btn)
        
        # Add Image
        add_btn = QtWidgets.QPushButton("Add Image(s)...")
        add_btn.clicked.connect(self.add_images)
        layout.addWidget(add_btn)
        # Remove Image
        remove_btn = QtWidgets.QPushButton("Remove Image...")
        remove_btn.clicked.connect(self.remove_image)
        layout.addWidget(remove_btn)

        # Restore defaults
        restore_btn = QtWidgets.QPushButton("Restore Defaults")
        restore_btn.clicked.connect(self.restore_defaults)
        layout.addWidget(restore_btn)

        # Apply
        apply_btn = QtWidgets.QPushButton("Apply")
        apply_btn.clicked.connect(self.accept)
        layout.addWidget(apply_btn)

        self.setLayout(layout)
        
    def select_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.config["border_color"] = color.name()
            
    def open_image_selector(self):
        from app.image_selector import ImageSelectorDialog
        shape = self.config.get("shape", "rectangle")
        current_squares = self.config.get("square_images", [])

        dialog = ImageSelectorDialog("images", current_squares, shape, self)
        if dialog.exec_():
            squares, circles = dialog.get_selected()
            self.config["square_images"] = squares
            self.config["circle_images"] = circles
            
    def add_images(self):
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Select Images", "", "Images (*.png *.jpg *.jpeg)")
        from app.image_utils import crop_image_square, crop_image_circle

        for path in files:
            if not os.path.exists(path):
                continue

            base_name = os.path.splitext(os.path.basename(path))[0]
            square_path = f"images/{base_name}_square.png"
            circle_path = f"images/{base_name}_circle.png"

            crop_image_square(path, square_path)
            crop_image_circle(square_path, circle_path)

            if square_path not in self.config["square_images"]:
                self.config["square_images"].append(square_path)
            if circle_path not in self.config["circle_images"]:
                self.config["circle_images"].append(circle_path)

    def remove_image(self):
        square_images = self.config.get("square_images", [])
        items = [os.path.basename(p) for p in square_images]
        if not items:
            QtWidgets.QMessageBox.information(self, "No Images", "There are no images to remove.")
            return

        item, ok = QtWidgets.QInputDialog.getItem(self, "Remove Image", "Select image to remove:", items, 0, False)
        if not ok or not item:
            return

        # Find the full square path from the selection
        square_path = next((p for p in square_images if os.path.basename(p) == item), None)
        if not square_path:
            return

        circle_path = square_path.replace("_square.png", "_circle.png")

        # Delete files
        for path in [square_path, circle_path]:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception as e:
                print(f"Error deleting {path}:", e)

        # Normalize paths before removing from config
        norm = lambda p: os.path.normpath(p).replace("\\", "/")
        square_path = norm(square_path)
        circle_path = norm(circle_path)

        self.config["square_images"] = [p for p in self.config["square_images"] if norm(p) != square_path]
        self.config["circle_images"] = [p for p in self.config["circle_images"] if norm(p) != circle_path]

        # Reset image index safely
        current_list = self.config["circle_images"] if self.config["shape"] == "circle" else self.config["square_images"]
        if not current_list:
            self.config["image_index"] = 0
        elif self.config["image_index"] >= len(current_list):
            self.config["image_index"] = 0



    def get_config(self):
        self.config["widget_opacity"] = self.opacity_slider.value() / 100
        self.config["widget_size"] = [self.width_box.value(), self.height_box.value()]
        self.config["shape"] = self.shape_combo.currentText()
        self.config["border_thickness"] = self.border_thickness.value()
        self.config["border_color"] = self.config.get("border_color", "#FF0000")
        return self.config

    def restore_defaults(self):
        with open("defaults.json", "r") as f:
            self.config.update(json.load(f))
        self.opacity_slider.setValue(int(self.config["widget_opacity"] * 100))
        self.width_box.setValue(self.config["widget_size"][0])
        self.height_box.setValue(self.config["widget_size"][1])
        self.shape_combo.setCurrentText(self.config["shape"])
        self.border_thickness.setValue(self.config["border_thickness"])
