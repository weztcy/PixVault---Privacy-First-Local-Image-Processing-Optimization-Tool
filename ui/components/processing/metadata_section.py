from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QComboBox
)


from .base_section import BaseProcessingSection




class MetadataSection(BaseProcessingSection):


    def __init__(
        self
    ):

        super().__init__(
            "Remove Metadata"
        )


        self.setup_content()



    def setup_content(
        self
    ):


        layout = QVBoxLayout()



        self.mode = QComboBox()

        self.mode.addItems(
            [
                "all",
                "custom"
            ]
        )



        layout.addWidget(
            QLabel(
                "Mode"
            )
        )


        layout.addWidget(
            self.mode
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
                "metadata",


            "mode":
                self.mode.currentText()

        }