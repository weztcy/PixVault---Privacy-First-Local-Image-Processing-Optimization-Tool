from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QSpinBox,
    QComboBox,
    QCheckBox
)


from .base_section import BaseProcessingSection




class DPISection(BaseProcessingSection):


    def __init__(
        self
    ):

        super().__init__(
            "DPI / Resolution"
        )


        self.setup_content()



    def setup_content(
        self
    ):

        layout = QVBoxLayout()



        self.unit = QComboBox()

        self.unit.addItems(
            [
                "DPI",
                "DPCM"
            ]
        )



        self.horizontal = QSpinBox()

        self.horizontal.setRange(
            1,
            2400
        )

        self.horizontal.setValue(
            300
        )



        self.vertical = QSpinBox()

        self.vertical.setRange(
            1,
            2400
        )

        self.vertical.setValue(
            300
        )



        self.link = QCheckBox(
            "Link Values"
        )


        self.link.setChecked(
            True
        )



        layout.addWidget(
            QLabel(
                "Unit"
            )
        )


        layout.addWidget(
            self.unit
        )


        layout.addWidget(
            QLabel(
                "Horizontal"
            )
        )


        layout.addWidget(
            self.horizontal
        )


        layout.addWidget(
            QLabel(
                "Vertical"
            )
        )


        layout.addWidget(
            self.vertical
        )


        layout.addWidget(
            self.link
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
                "dpi",


            "unit":
                self.unit.currentText(),


            "horizontal":
                self.horizontal.value(),


            "vertical":
                self.vertical.value()

        }