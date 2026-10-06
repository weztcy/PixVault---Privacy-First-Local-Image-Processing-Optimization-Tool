from PySide6.QtWidgets import (
    QLabel,
    QCheckBox,
    QSlider,
    QComboBox,
    QLineEdit
)


from PySide6.QtCore import (
    Qt
)


from ui.components.format_options.base_format_options import (
    BaseFormatOptions
)





class GIFOptions(
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
        # COLORS
        # =====================


        self.add_widget(

            QLabel(
                "Color Count"
            )

        )


        self.colors = QSlider(

            Qt.Orientation.Horizontal

        )


        self.colors.setRange(

            2,

            256

        )


        self.colors.setValue(

            256

        )


        self.add_widget(

            self.colors

        )









        # =====================
        # DITHER
        # =====================


        self.add_widget(

            QLabel(
                "Dithering"
            )

        )


        self.dither = QComboBox()



        self.dither.addItems(

            [

                "none",

                "floyd_steinberg",

                "ordered",

                "atkinson"

            ]

        )


        self.dither.setCurrentText(

            "floyd_steinberg"

        )


        self.add_widget(

            self.dither

        )









        # =====================
        # OPTIMIZE
        # =====================


        self.optimize = QCheckBox(

            "Optimize GIF"

        )


        self.optimize.setChecked(

            True

        )


        self.add_widget(

            self.optimize

        )









        # =====================
        # LOOP
        # =====================


        self.loop = QCheckBox(

            "Enable Animation Loop"

        )


        self.loop.setChecked(

            True

        )


        self.add_widget(

            self.loop

        )









        # =====================
        # LOOP COUNT
        # =====================


        self.add_widget(

            QLabel(
                "Loop Count (0 = infinite)"
            )

        )


        self.loop_count = QLineEdit(

            "0"

        )


        self.add_widget(

            self.loop_count

        )









        # =====================
        # TRANSPARENCY
        # =====================


        self.transparency = QCheckBox(

            "Enable Transparency"

        )


        self.transparency.setChecked(

            True

        )


        self.add_widget(

            self.transparency

        )









        # =====================
        # FRAME DURATION
        # =====================


        self.add_widget(

            QLabel(
                "Frame Duration (ms)"
            )

        )


        self.duration = QLineEdit(

            "100"

        )


        self.add_widget(

            self.duration

        )









    def get_settings(
        self
    ):


        return {


            "colors":

                self.colors.value(),



            "dither":

                self.dither.currentText(),



            "optimize":

                self.optimize.isChecked(),



            "loop":

                self.loop.isChecked(),



            "loop_count":

                self.loop_count.text(),



            "transparency":

                self.transparency.isChecked(),



            "duration":

                self.duration.text()

        }









    def reset(
        self
    ):


        self.colors.setValue(

            256

        )


        self.dither.setCurrentText(

            "floyd_steinberg"

        )


        self.optimize.setChecked(

            True

        )


        self.loop.setChecked(

            True

        )


        self.loop_count.setText(

            "0"

        )


        self.transparency.setChecked(

            True

        )


        self.duration.setText(

            "100"

        )