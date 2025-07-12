import os
import zipfile
import requests
import shutil
import subprocess
from pathlib import Path
from PyQt5 import QtWidgets
import sys

GITHUB_ZIP_URL = "https://github.com/Ryan-A-V/SunWidget/archive/refs/heads/master.zip"
APP_NAME = "SunWidget"
APPDATA_PATH = Path(os.getenv("APPDATA")) / APP_NAME
STARTUP_PATH = Path(os.getenv("APPDATA")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"

def download_and_extract():
    print("[*] Downloading widget files...")
    zip_path = APPDATA_PATH / "widget.zip"
    os.makedirs(APPDATA_PATH, exist_ok=True)

    r = requests.get(GITHUB_ZIP_URL, stream=True)
    with open(zip_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    print("[*] Extracting files...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(APPDATA_PATH)

    folders = [f for f in APPDATA_PATH.iterdir()]
    if not folders:
        raise RuntimeError("Extraction failed: Main folder not found.")

    extracted_dir = folders[0]

    for item in extracted_dir.iterdir():
        shutil.move(str(item), str(APPDATA_PATH))

    shutil.rmtree(extracted_dir)
    os.remove(zip_path)

def create_shortcut(path, target):
    from win32com.client import Dispatch
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(path))
    shortcut.Targetpath = str(target)
    shortcut.WorkingDirectory = str(target.parent)
    shortcut.IconLocation = str(target)
    shortcut.save()

def create_startup_shortcut():
    target = APPDATA_PATH / "main.py"
    shortcut_path = STARTUP_PATH / f"{APP_NAME}.lnk"
    create_shortcut(shortcut_path, target)

def create_desktop_shortcut():
    desktop = Path(os.path.join(os.environ["USERPROFILE"], "Desktop"))
    shortcut_path = desktop / f"{APP_NAME}.lnk"
    target = APPDATA_PATH / "main.py"
    create_shortcut(shortcut_path, target)

def run_widget():
    subprocess.Popen(["pythonw", str(APPDATA_PATH / "main.py")], cwd=str(APPDATA_PATH))

class InstallerWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SunWidget Installer")
        self.setFixedSize(400, 250)

        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(QtWidgets.QLabel("<h2>☀️ Thanks for downloading SunWidget!</h2>"))
        layout.addWidget(QtWidgets.QLabel("A floating desktop widget to showcase your best images."))

        self.desktop_checkbox = QtWidgets.QCheckBox("Add shortcut to desktop")
        self.desktop_checkbox.setChecked(True)
        layout.addWidget(self.desktop_checkbox)

        self.install_btn = QtWidgets.QPushButton("Install")
        self.install_btn.clicked.connect(self.install)
        layout.addWidget(self.install_btn)

        self.status_label = QtWidgets.QLabel("")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def install(self):
        self.status_label.setText("Installing...")
        QtWidgets.qApp.processEvents()

        try:
            download_and_extract()
            create_startup_shortcut()
            if self.desktop_checkbox.isChecked():
                create_desktop_shortcut()
            self.status_label.setText("Installed successfully! Launching SunWidget...")
            run_widget()
            self.close()
        except Exception as e:
            self.status_label.setText(f"Install failed: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = InstallerWindow()
    win.show()
    sys.exit(app.exec_())
