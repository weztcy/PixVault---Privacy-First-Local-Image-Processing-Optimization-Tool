from PySide6.QtWidgets import QComboBox, QLabel

from ui.components.processing_options.base_processing_options import (
    BaseProcessingOptions,
)


class BitDepthOptions(BaseProcessingOptions):
    BIT_DEPTHS = ["8-bit", "16-bit", "32-bit"]

    def __init__(self):

        super().__init__()

    def setup_ui(self):

        super().setup_ui()

        self.add_widget(QLabel("Bit Depth"))

        self.bit_depth = QComboBox()

        self.bit_depth.addItems(self.BIT_DEPTHS)

        self.bit_depth.setCurrentText("8-bit")

        self.add_widget(self.bit_depth)

    def get_settings(self):

        value = self.bit_depth.currentText().replace("-bit", "")

        return {"type": "bitdepth", "value": int(value)}

    def reset(self):

        self.bit_depth.setCurrentText("8-bit")

    def update_capability(self):

        unsupported = []

        if self.current_format in ["JPEG", "WEBP", "GIF", "ICO"]:
            unsupported = ["16-bit", "32-bit"]

        elif (
            self.current_format in ["PNG"]
            or self.current_format in ["AVIF", "HEIC", "HEIF"]
            or self.current_format in ["BMP"]
        ):
            unsupported = ["32-bit"]

        for index in range(self.bit_depth.count()):
            item = self.bit_depth.itemText(index)

            enabled = item not in unsupported

            self.bit_depth.model().item(index).setEnabled(enabled)

        current = self.bit_depth.currentText()

        if current in unsupported:
            self.bit_depth.setCurrentText("8-bit")

            self.show_warning(f"{self.current_format} does not support {current}.")

        elif unsupported:
            self.show_warning(f"{self.current_format} has limited bit depth support.")

        else:
            self.show_warning("")
