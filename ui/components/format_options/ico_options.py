from PySide6.QtWidgets import (
    QLabel,
    QCheckBox,
    QComboBox
)


from ui.components.format_options.base_format_options import (
    BaseFormatOptions
)





class ICOOptions(
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
        # ICON SIZE
        # =====================


        self.add_widget(

            QLabel(
                "Icon Size"
            )

        )


        self.size = QComboBox()



        self.size.addItems(

            [

                "16",

                "32",

                "48",

                "64",

                "128",

                "256"

            ]

        )


        self.size.setCurrentText(

            "256"

        )


        self.add_widget(

            self.size

        )









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

                "24",

                "32"

            ]

        )


        self.bit_depth.setCurrentText(

            "32"

        )


        self.add_widget(

            self.bit_depth

        )









        # =====================
        # ALPHA
        # =====================


        self.alpha = QCheckBox(

            "Preserve Alpha Channel"

        )


        self.alpha.setChecked(

            True

        )


        self.add_widget(

            self.alpha

        )









        # =====================
        # MULTI SIZE
        # =====================


        self.multiple_sizes = QCheckBox(

            "Generate Multiple Icon Sizes"

        )


        self.multiple_sizes.setChecked(

            True

        )


        self.add_widget(

            self.multiple_sizes

        )









    def get_settings(
        self
    ):


        return {


            "size":

                int(

                    self.size.currentText()

                ),



            "bit_depth":

                int(

                    self.bit_depth.currentText()

                ),



            "alpha":

                self.alpha.isChecked(),



            "multiple_sizes":

                self.multiple_sizes.isChecked()

        }









    def reset(
        self
    ):


        self.size.setCurrentText(

            "256"

        )


        self.bit_depth.setCurrentText(

            "32"

        )


        self.alpha.setChecked(

            True

        )


        self.multiple_sizes.setChecked(

            True

        )