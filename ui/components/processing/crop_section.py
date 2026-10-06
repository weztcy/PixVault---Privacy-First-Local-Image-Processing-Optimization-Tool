from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QComboBox
)


from .base_section import BaseProcessingSection




class CropSection(BaseProcessingSection):


    def __init__(
        self
    ):

        super().__init__(
            "Crop"
        )


        self.setup_content()



    def setup_content(
        self
    ):


        layout = QVBoxLayout()



        self.mode = QComboBox()

        self.mode.addItems(
            [
                "aspect_ratio",
                "fixed",
                "percentage",
                "custom"
            ]
        )



        self.ratio = QComboBox()

        self.ratio.addItems(
            [
                "16:9",
                "4:3",
                "1:1"
            ]
        )



        layout.addWidget(
            QLabel(
                "Crop Mode"
            )
        )


        layout.addWidget(
            self.mode
        )



        layout.addWidget(
            QLabel(
                "Aspect Ratio"
            )
        )


        layout.addWidget(
            self.ratio
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
                "crop",


            "mode":
                self.mode.currentText(),


            "ratio":
                self.ratio.currentText()

        }