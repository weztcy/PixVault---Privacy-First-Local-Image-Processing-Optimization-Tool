from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QComboBox
)


from .base_section import BaseProcessingSection




class TransformSection(BaseProcessingSection):


    def __init__(
        self
    ):

        super().__init__(
            "Transform"
        )


        self.setup_content()



    def setup_content(
        self
    ):


        layout = QVBoxLayout()



        self.rotation = QComboBox()

        self.rotation.addItems(
            [
                "none",
                "90",
                "180",
                "270"
            ]
        )



        self.flip = QComboBox()

        self.flip.addItems(
            [
                "none",
                "horizontal",
                "vertical",
                "both"
            ]
        )



        layout.addWidget(
            QLabel(
                "Rotation"
            )
        )


        layout.addWidget(
            self.rotation
        )



        layout.addWidget(
            QLabel(
                "Flip"
            )
        )


        layout.addWidget(
            self.flip
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
                "transform",


            "rotation":
                self.rotation.currentText(),


            "flip":
                self.flip.currentText()

        }