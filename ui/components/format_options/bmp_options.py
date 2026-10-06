from PySide6.QtWidgets import (
    QLabel,
    QCheckBox,
    QComboBox
)


from ui.components.format_options.base_format_options import (
    BaseFormatOptions
)





class BMPOptions(
    BaseFormatOptions
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
        # BIT DEPTH
        # =====================


        self.add_widget(

            QLabel(
                "Bit Depth"
            )

        )


        self.bit_depth = QComboBox()



        self.bit_depth.addItems(

            [

                "1",

                "4",

                "8",

                "16",

                "24",

                "32"

            ]

        )


        self.bit_depth.setCurrentText(

            "24"

        )


        self.add_widget(

            self.bit_depth

        )









        # =====================
        # ALPHA
        # =====================


        self.alpha = QCheckBox(

            "Enable Alpha Channel"

        )


        self.alpha.setChecked(

            False

        )


        self.add_widget(

            self.alpha

        )









        # =====================
        # COMPRESSION
        # =====================


        self.add_widget(

            QLabel(
                "Compression"
            )

        )


        self.compression = QComboBox()



        self.compression.addItems(

            [

                "none",

                "rle"

            ]

        )


        self.compression.setCurrentText(

            "none"

        )


        self.add_widget(

            self.compression

        )









        # =====================
        # ORIENTATION
        # =====================


        self.top_down = QCheckBox(

            "Top Down Orientation"

        )


        self.top_down.setChecked(

            False

        )


        self.add_widget(

            self.top_down

        )









    def get_settings(
        self
    ):


        return {


            "bit_depth":

                int(

                    self.bit_depth.currentText()

                ),



            "alpha":

                self.alpha.isChecked(),



            "compression":

                self.compression.currentText(),



            "top_down":

                self.top_down.isChecked()

        }









    def reset(
        self
    ):


        self.bit_depth.setCurrentText(

            "24"

        )


        self.alpha.setChecked(

            False

        )


        self.compression.setCurrentText(

            "none"

        )


        self.top_down.setChecked(

            False

        )