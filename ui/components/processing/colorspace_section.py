from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QComboBox
)


from .base_section import BaseProcessingSection




class ColorSpaceSection(BaseProcessingSection):


    def __init__(
        self
    ):

        super().__init__(
            "Color Space"
        )


        self.setup_content()



    def setup_content(
        self
    ):


        layout = QVBoxLayout()



        self.target = QComboBox()

        self.target.addItems(
            [
                "sRGB",
                "Adobe RGB",
                "Display P3",
                "CMYK",
                "Grayscale"
            ]
        )



        self.intent = QComboBox()

        self.intent.addItems(
            [
                "Perceptual",
                "Relative Colorimetric",
                "Saturation",
                "Absolute Colorimetric"
            ]
        )



        layout.addWidget(
            QLabel(
                "Convert To"
            )
        )


        layout.addWidget(
            self.target
        )


        layout.addWidget(
            QLabel(
                "Rendering Intent"
            )
        )


        layout.addWidget(
            self.intent
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
                "colorspace",


            "target":
                self.target.currentText(),


            "intent":
                self.intent.currentText()

        }