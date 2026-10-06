from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QComboBox
)


from .base_section import BaseProcessingSection




class BitDepthSection(BaseProcessingSection):


    def __init__(
        self
    ):

        super().__init__(
            "Bit Depth"
        )


        self.setup_content()



    def setup_content(
        self
    ):


        layout = QVBoxLayout()



        self.depth = QComboBox()

        self.depth.addItems(
            [
                "8",
                "16",
                "32"
            ]
        )



        layout.addWidget(
            QLabel(
                "Output Bit Depth"
            )
        )


        layout.addWidget(
            self.depth
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
                "bitdepth",


            "value":
                int(
                    self.depth.currentText()
                )

        }