☀️ SunWidget

SunWidget is a floating desktop widget for Windows that cycles through images with customizable styles, shapes, and border settings. Built with PyQt5, it supports hot-swappable image sets, persistent configuration, and a polished installer experience.

---

🚀 Features

- Auto-cycling image widget (click to cycle, long-click to move with shake)
- Square or circle display shape (cropped automatically)
- Right-click to open full settings UI
- Per-image selector window with previews
- Persistent JSON-based settings
- Add/remove images from settings (auto-cropped on add)
- Border color, opacity, thickness, and widget opacity control
- "Restore Defaults" button
- Automatic startup (via shortcut)
- Optional desktop shortcut
- Full installer + uninstaller included

---

🧠 Requirements

- Windows 10 or 11
- Python 3.8+
- pip install pyqt5 pywin32 requests

---

🧰 Installation Options

🔹 Option 1: Use the Installer (Recommended)

1. Download SunWidget_Installer_With_Uninstaller.zip
2. Extract it anywhere
3. Run:
   python install_gui.py
4. ✅ You're done! SunWidget will:
   - Install to %APPDATA%/SunWidget
   - Launch automatically
   - Create a desktop shortcut (optional)

To uninstall:
   python uninstall_gui.py

---

🔸 Option 2: Manual Setup (Dev Mode)

1. Clone the repo:
   git clone https://github.com/Ryan-A-V/SunWidget.git
   cd SunWidget

2. Install dependencies:
   pip install pyqt5 pywin32 requests

3. Run the widget:
   python main.py

Settings are stored persistently in settings.json in the app directory.

---

🧪 Testing in a VM

On Windows 11 Home, we recommend using VirtualBox + the official Windows 11 ISO.

1. Download ISO: https://www.microsoft.com/software-download/windows11
2. Install VirtualBox
3. Create a VM and mount the ISO
4. Drag SunWidget_Installer_With_Uninstaller.zip into the VM
5. Install & verify persistence

---

📜 License

This project is licensed under the MIT License.
Feel free to fork, remix, and use — but don’t sell it as-is without adding value or changing it.

---

🧡 Thanks for trying SunWidget!
