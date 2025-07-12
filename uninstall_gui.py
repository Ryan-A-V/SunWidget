import os
import shutil
import subprocess
from pathlib import Path
from PyQt5 import QtWidgets
import sys

APP_NAME = "SunWidget"
APPDATA_PATH = Path(os.getenv("APPDATA")) / APP_NAME
STARTUP_PATH = Path(os.getenv("APPDATA")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
DESKTOP_PATH = Path(os.path.join(os.environ["USERPROFILE"], "Desktop"))

def full_cleanup():
    # Kill any running pythonw.exe (SunWidget)
    try:
        subprocess.run(["taskkill", "/f", "/im", "pythonw.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

    # Delete desktop and startup shortcuts
    desktop = Path(os.path.join(os.environ["USERPROFILE"], "Desktop"))
    startup = Path(os.getenv("APPDATA")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"

    desktop_shortcut = desktop / f"{APP_NAME}.lnk"
    startup_shortcut = startup / f"{APP_NAME}.lnk"

    for shortcut in [desktop_shortcut, startup_shortcut]:
        try:
            if shortcut.exists():
                shortcut.unlink()
        except Exception:
            pass

    # Delete the entire app folder
    try:
        if APPDATA_PATH.exists():
            shutil.rmtree(APPDATA_PATH, ignore_errors=True)
    except Exception:
        pass


def remove_file(path):
    try:
        if path.exists():
            path.unlink()
            print(f"Removed: {path}")
    except Exception as e:
        print(f"Failed to remove {path}: {e}")

def remove_folder(path):
    try:
        if path.exists():
            shutil.rmtree(path)
            print(f"Removed folder: {path}")
    except Exception as e:
        print(f"Failed to remove folder {path}: {e}")

class UninstallerWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Uninstall SunWidget")
        self.setFixedSize(350, 180)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Are you sure you want to uninstall SunWidget?"))
        layout.addWidget(QtWidgets.QLabel("This will delete all app files and shortcuts."))

        btn_layout = QtWidgets.QHBoxLayout()
        yes_btn = QtWidgets.QPushButton("Yes, uninstall")
        no_btn = QtWidgets.QPushButton("Cancel")

        yes_btn.clicked.connect(self.uninstall)
        no_btn.clicked.connect(self.close)

        btn_layout.addWidget(yes_btn)
        btn_layout.addWidget(no_btn)
        layout.addLayout(btn_layout)

        self.status_label = QtWidgets.QLabel("")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def uninstall(self):
        full_cleanup()
        self.status_label.setText("Uninstalled successfully.")
        QtWidgets.QApplication.instance().quit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = UninstallerWindow()
    win.show()
    sys.exit(app.exec_())
