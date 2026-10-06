from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QSpinBox
)


from .base_section import BaseProcessingSection




class CompressionSection(BaseProcessingSection):


    def __init__(
        self
    ):

        super().__init__(
            "Compression"
        )


        self.setup_content()



    def setup_content(
        self
    ):


        layout = QVBoxLayout()



        self.quality = QSpinBox()

        self.quality.setRange(
            1,
            100
        )


        self.quality.setValue(
            85
        )



        layout.addWidget(
            QLabel(
                "Quality"
            )
        )


        layout.addWidget(
            self.quality
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
                "compression",


            "quality":
                self.quality.value()

        }