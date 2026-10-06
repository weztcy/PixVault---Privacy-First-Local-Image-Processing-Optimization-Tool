from PySide6.QtWidgets import (
    QLabel,
    QCheckBox,
    QSlider,
    QComboBox
)


from PySide6.QtCore import (
    Qt
)


from ui.components.format_options.base_format_options import (
    BaseFormatOptions
)





class PNGOptions(
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
        # COMPRESSION LEVEL
        # =====================


        self.add_widget(

            QLabel(
                "Compression Level"
            )

        )



        self.compression_level = QSlider(

            Qt.Orientation.Horizontal

        )


        self.compression_level.setRange(

            0,

            9

        )


        self.compression_level.setValue(

            6

        )



        self.add_widget(

            self.compression_level

        )







        # =====================
        # OPTIMIZE
        # =====================


        self.optimize = QCheckBox(

            "Optimize PNG"

        )


        self.optimize.setChecked(

            True

        )


        self.add_widget(

            self.optimize

        )







        # =====================
        # INTERLACE
        # =====================


        self.interlace = QCheckBox(

            "Interlaced PNG"

        )


        self.interlace.setChecked(

            False

        )


        self.add_widget(

            self.interlace

        )







        # =====================
        # FILTER
        # =====================


        self.add_widget(

            QLabel(
                "Filter Strategy"
            )

        )



        self.filter_mode = QComboBox()



        self.filter_mode.addItems(

            [

                "none",

                "sub",

                "up",

                "average",

                "paeth",

                "adaptive"

            ]

        )



        self.filter_mode.setCurrentText(

            "adaptive"

        )



        self.add_widget(

            self.filter_mode

        )









    def get_settings(
        self
    ):


        return {


            "compression_level":

                self.compression_level.value(),



            "optimize":

                self.optimize.isChecked(),



            "interlace":

                self.interlace.isChecked(),



            "filter":

                self.filter_mode.currentText()

        }









    def reset(
        self
    ):


        self.compression_level.setValue(

            6

        )


        self.optimize.setChecked(

            True

        )


        self.interlace.setChecked(

            False

        )


        self.filter_mode.setCurrentText(

            "adaptive"

        )