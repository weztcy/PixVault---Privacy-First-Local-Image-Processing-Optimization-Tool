from PySide6.QtWidgets import QCheckBox, QComboBox, QLabel, QSpinBox

from ui.components.processing_options.base_processing_options import (
    BaseProcessingOptions,
)


class ResizeOptions(BaseProcessingOptions):
    def __init__(self):

        super().__init__()

    def setup_ui(self):

        super().setup_ui()

        # =====================
        # METHOD
        # =====================

        self.add_widget(QLabel("Resize Method"))

        self.method = QComboBox()

        self.method.addItems(
            [
                "Exact Dimensions",
                "Width",
                "Height",
                "Longest Side",
                "Shortest Side",
                "Percentage",
            ]
        )

        self.add_widget(self.method)

        # =====================
        # VALUE 1
        # =====================

        self.width_label = QLabel("Width")

        self.width_input = QSpinBox()

        self.width_input.setRange(1, 100000)

        self.add_widget(self.width_label)

        self.add_widget(self.width_input)

        # =====================
        # VALUE 2
        # =====================

        self.height_label = QLabel("Height")

        self.height_input = QSpinBox()

        self.height_input.setRange(1, 100000)

        self.add_widget(self.height_label)

        self.add_widget(self.height_input)

        # =====================
        # PERCENTAGE
        # =====================

        self.percentage_label = QLabel("Percentage (%)")

        self.percentage_input = QSpinBox()

        self.percentage_input.setRange(1, 1000)

        self.percentage_input.setValue(100)

        self.add_widget(self.percentage_label)

        self.add_widget(self.percentage_input)

        # =====================
        # ASPECT RATIO
        # =====================

        self.keep_ratio = QCheckBox("Keep Aspect Ratio")

        self.keep_ratio.setChecked(True)

        self.add_widget(self.keep_ratio)

        # =====================
        # RESAMPLING
        # =====================

        self.add_widget(QLabel("Resampling"))

        self.resampling = QComboBox()

        self.resampling.addItems(["Nearest", "Bilinear", "Bicubic", "Lanczos"])

        self.resampling.setCurrentText("Lanczos")

        self.add_widget(self.resampling)

        self.method.currentTextChanged.connect(self.update_ui)

        self.update_ui()

    def update_ui(self):

        method = self.method.currentText()

        exact = method == "Exact Dimensions"

        width_mode = method == "Width"

        height_mode = method == "Height"

        percentage = method == "Percentage"

        side_mode = method in ["Longest Side", "Shortest Side"]

        self.width_label.setVisible(exact or width_mode)

        self.width_input.setVisible(exact or width_mode)

        self.height_label.setVisible(exact or height_mode)

        self.height_input.setVisible(exact or height_mode)

        self.percentage_label.setVisible(percentage)

        self.percentage_input.setVisible(percentage)

        self.keep_ratio.setEnabled(not exact)

        if exact:
            self.keep_ratio.setChecked(False)

    def get_settings(self):

        method_map = {
            "Exact Dimensions": "exact",
            "Width": "width",
            "Height": "height",
            "Longest Side": "longest_side",
            "Shortest Side": "shortest_side",
            "Percentage": "percentage",
        }

        settings = {
            "type": "resize",
            "method": method_map[self.method.currentText()],
            "keep_ratio": self.keep_ratio.isChecked(),
            "resampling": self.resampling.currentText().lower(),
        }

        method = settings["method"]

        if method == "exact":
            settings["width"] = self.width_input.value()

            settings["height"] = self.height_input.value()

        elif method in ["width", "height", "longest_side", "shortest_side"]:
            settings["value"] = self.width_input.value()

        elif method == "percentage":
            settings["value"] = self.percentage_input.value()

        return settings

    def reset(self):

        self.method.setCurrentText("Width")

        self.width_input.setValue(1000)

        self.height_input.setValue(1000)

        self.percentage_input.setValue(100)

        self.keep_ratio.setChecked(True)

        self.resampling.setCurrentText("Lanczos")

        self.update_ui()

    def update_capability(self):

        if self.current_format == "SVG":
            self.show_warning("SVG resize depends on renderer implementation.")

        else:
            self.show_warning("")
