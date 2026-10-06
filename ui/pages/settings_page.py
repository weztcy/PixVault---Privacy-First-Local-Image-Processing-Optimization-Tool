import json
from pathlib import Path

from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class SettingsPage(QWidget):
    SETTINGS_FILE = Path("config/app_settings.json")

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.load_settings()

    def setup_ui(self):

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Settings"))

        # =====================
        # FORMAT
        # =====================

        layout.addWidget(QLabel("Default Output Format"))

        self.format_box = QComboBox()

        self.format_box.addItems(["WEBP", "JPEG", "PNG", "AVIF", "TIFF", "HEIC"])

        layout.addWidget(self.format_box)

        # =====================
        # QUALITY
        # =====================

        layout.addWidget(QLabel("Default Quality"))

        self.quality_spin = QSpinBox()

        self.quality_spin.setRange(1, 100)

        self.quality_spin.setValue(85)

        layout.addWidget(self.quality_spin)

        # =====================
        # OUTPUT FOLDER
        # =====================

        layout.addWidget(QLabel("Default Output Folder"))

        self.output_folder = QLineEdit()

        browse = QPushButton("Select Folder")

        browse.clicked.connect(self.select_folder)

        layout.addWidget(self.output_folder)

        layout.addWidget(browse)

        # =====================
        # SAVE
        # =====================

        save = QPushButton("Save Settings")

        save.clicked.connect(self.save_settings)

        layout.addWidget(save)

        self.status_label = QLabel()

        layout.addWidget(self.status_label)

        layout.addStretch()

        self.setLayout(layout)

    def select_folder(self):

        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")

        if folder:
            self.output_folder.setText(folder)

    def load_settings(self):

        if not self.SETTINGS_FILE.exists():
            return

        try:
            with open(self.SETTINGS_FILE, "r", encoding="utf-8") as file:
                settings = json.load(file)

            format_name = settings.get("format")

            if format_name:
                index = self.format_box.findText(format_name)

                if index >= 0:
                    self.format_box.setCurrentIndex(index)

            self.quality_spin.setValue(settings.get("quality", 85))

            self.output_folder.setText(settings.get("output_folder", ""))

        except Exception:
            pass

    def save_settings(self):

        folder = self.output_folder.text().strip()

        if folder and not Path(folder).exists():
            QMessageBox.warning(self, "Invalid Folder", "Output folder does not exist.")

            return

        settings = {
            "format": self.format_box.currentText(),
            "quality": self.quality_spin.value(),
            "output_folder": folder,
        }

        try:
            self.SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)

            with open(self.SETTINGS_FILE, "w", encoding="utf-8") as file:
                json.dump(settings, file, indent=4)

            self.status_label.setText("Settings saved")

        except Exception as error:
            QMessageBox.critical(self, "Save Error", str(error))
