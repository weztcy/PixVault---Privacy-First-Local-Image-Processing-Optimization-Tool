from PySide6.QtWidgets import (
    QLabel,
    QComboBox,
    QSpinBox,
    QCheckBox
)


from ui.components.processing_options.base_processing_options import (
    BaseProcessingOptions
)






class DPIOptions(
    BaseProcessingOptions
):


    def __init__(
        self
    ):

        super().__init__()







    def setup_ui(
        self
    ):


        super().setup_ui()



        # =====================
        # UNIT
        # =====================


        self.add_widget(

            QLabel(
                "Resolution Unit"
            )

        )


        self.unit = QComboBox()


        self.unit.addItems(

            [

                "DPI",

                "DPCM"

            ]

        )


        self.add_widget(

            self.unit

        )






        # =====================
        # HORIZONTAL
        # =====================


        self.add_widget(

            QLabel(
                "Horizontal Resolution"
            )

        )


        self.horizontal = QSpinBox()


        self.horizontal.setRange(

            1,

            10000

        )


        self.horizontal.setValue(

            300

        )


        self.add_widget(

            self.horizontal

        )







        # =====================
        # VERTICAL
        # =====================


        self.add_widget(

            QLabel(
                "Vertical Resolution"
            )

        )


        self.vertical = QSpinBox()


        self.vertical.setRange(

            1,

            10000

        )


        self.vertical.setValue(

            300

        )


        self.add_widget(

            self.vertical

        )







        # =====================
        # LINK
        # =====================


        self.link = QCheckBox(

            "Keep Horizontal & Vertical Linked"

        )


        self.link.setChecked(

            True

        )


        self.add_widget(

            self.link

        )





        self.horizontal.valueChanged.connect(

            self.sync_vertical

        )


        self.vertical.valueChanged.connect(

            self.sync_horizontal

        )









    def sync_vertical(
        self,
        value
    ):


        if self.link.isChecked():


            self.vertical.blockSignals(

                True

            )


            self.vertical.setValue(

                value

            )


            self.vertical.blockSignals(

                False

            )









    def sync_horizontal(
        self,
        value
    ):


        if self.link.isChecked():


            self.horizontal.blockSignals(

                True

            )


            self.horizontal.setValue(

                value

            )


            self.horizontal.blockSignals(

                False

            )









    def get_settings(
        self
    ):


        return {


            "type":

                "dpi",


            "unit":

                self.unit.currentText().lower(),



            "horizontal":

                self.horizontal.value(),



            "vertical":

                self.vertical.value()

        }









    def reset(
        self
    ):


        self.unit.setCurrentText(

            "DPI"

        )


        self.horizontal.setValue(

            300

        )


        self.vertical.setValue(

            300

        )


        self.link.setChecked(

            True

        )









    def update_capability(
        self
    ):


        if self.current_format == "SVG":


            self.setEnabled(

                False

            )


            self.show_warning(

                "SVG does not use DPI. Use vector dimensions instead."

            )


        else:


            self.setEnabled(

                True

            )


            self.show_warning(

                ""

            )