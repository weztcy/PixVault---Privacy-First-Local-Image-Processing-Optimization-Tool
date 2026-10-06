from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QComboBox,
    QSpinBox,
    QCheckBox
)


from .base_section import BaseProcessingSection




class ResizeSection(BaseProcessingSection):


    def __init__(
        self
    ):

        super().__init__(
            "Resize"
        )


        self.setup_content()



    def setup_content(
        self
    ):


        layout = QVBoxLayout()



        self.method = QComboBox()

        self.method.addItems(
            [
                "width",
                "height",
                "percentage",
                "longest_side",
                "shortest_side"
            ]
        )



        self.value = QSpinBox()

        self.value.setRange(
            1,
            10000
        )


        self.value.setValue(
            1920
        )



        self.keep_ratio = QCheckBox(
            "Keep Aspect Ratio"
        )


        self.keep_ratio.setChecked(
            True
        )



        layout.addWidget(
            QLabel(
                "Resize Method"
            )
        )


        layout.addWidget(
            self.method
        )



        layout.addWidget(
            QLabel(
                "Value"
            )
        )


        layout.addWidget(
            self.value
        )



        layout.addWidget(
            self.keep_ratio
        )



        self.set_content_layout(
            layout
        )



    def get_config(
        self
    ):


        if not self.enabled():

            return None



        return {

            "type":
                "resize",


            "method":
                self.method.currentText(),


            "value":
                self.value.value(),


            "keep_ratio":
                self.keep_ratio.isChecked()

        }