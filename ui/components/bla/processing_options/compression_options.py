from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QLabel, QSlider, QSpinBox

from ui.components.processing_options.base_processing_options import (
    BaseProcessingOptions,
)


class CompressionOptions(BaseProcessingOptions):
    def __init__(self):

        super().__init__()

    def setup_ui(self):

        super().setup_ui()

        # =====================
        # MODE
        # =====================

        self.add_widget(QLabel("Compression Mode"))

        self.mode = QComboBox()

        self.mode.addItems(["Quality", "Target File Size"])

        self.add_widget(self.mode)

        # =====================
        # QUALITY
        # =====================

        self.quality_label = QLabel("Quality")

        self.quality = QSlider(Qt.Orientation.Horizontal)

        self.quality.setRange(1, 100)

        self.quality.setValue(85)

        self.add_widget(self.quality_label)

        self.add_widget(self.quality)

        # =====================
        # TARGET SIZE
        # =====================

        self.size_label = QLabel("Target Size")

        self.size = QSpinBox()

        self.size.setRange(1, 1000000)

        self.size.setValue(1024)

        self.unit = QComboBox()

        self.unit.addItems(["KB", "MB"])

        self.accuracy = QComboBox()

        self.accuracy.addItems(["Prioritize Size", "Balanced", "Prioritize Quality"])

        self.add_widget(self.size_label)

        self.add_widget(self.size)

        self.add_widget(self.unit)

        self.add_widget(QLabel("Target Accuracy"))

        self.add_widget(self.accuracy)

        self.mode.currentTextChanged.connect(self.update_ui)

        self.update_ui()

    def update_ui(self):

        quality_mode = self.mode.currentText() == "Quality"

        self.quality_label.setVisible(quality_mode)

        self.quality.setVisible(quality_mode)

        self.size_label.setVisible(not quality_mode)

        self.size.setVisible(not quality_mode)

        self.unit.setVisible(not quality_mode)

        self.accuracy.setVisible(not quality_mode)

    def get_settings(self):

        if self.mode.currentText() == "Quality":
            return {
                "type": "compression",
                "mode": "quality",
                "quality": self.quality.value(),
            }

        return {
            "type": "compression",
            "mode": "target_size",
            "size": self.size.value(),
            "unit": self.unit.currentText().lower(),
            "accuracy": self.accuracy.currentText(),
        }

    def reset(self):

        self.mode.setCurrentText("Quality")

        self.quality.setValue(85)

        self.size.setValue(1024)

        self.unit.setCurrentText("KB")

        self.accuracy.setCurrentText("Balanced")

        self.update_ui()

    def update_capability(self):

        unsupported_quality = ["PNG", "GIF", "BMP", "ICO", "SVG"]

        if self.current_format in unsupported_quality:
            self.mode.setCurrentText("Target File Size")

            self.mode.model().item(0).setEnabled(False)

            self.show_warning(
                f"{self.current_format} does not support quality compression."
            )

        else:
            self.mode.model().item(0).setEnabled(True)

            self.show_warning("")
