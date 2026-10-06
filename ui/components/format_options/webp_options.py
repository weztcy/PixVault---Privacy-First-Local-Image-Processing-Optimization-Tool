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





class WEBPOptions(
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
        # LOSSLESS
        # =====================


        self.lossless = QCheckBox(

            "Lossless Compression"

        )


        self.lossless.setChecked(

            False

        )


        self.add_widget(

            self.lossless

        )







        # =====================
        # QUALITY
        # =====================


        self.add_widget(

            QLabel(
                "Quality"
            )

        )


        self.quality = QSlider(

            Qt.Orientation.Horizontal

        )


        self.quality.setRange(

            1,

            100

        )


        self.quality.setValue(

            85

        )


        self.add_widget(

            self.quality

        )







        # =====================
        # METHOD
        # =====================


        self.add_widget(

            QLabel(
                "Compression Method"
            )

        )



        self.method = QComboBox()



        self.method.addItems(

            [

                "0",

                "1",

                "2",

                "3",

                "4",

                "5",

                "6"

            ]

        )


        self.method.setCurrentText(

            "4"

        )


        self.add_widget(

            self.method

        )







        # =====================
        # ALPHA QUALITY
        # =====================


        self.add_widget(

            QLabel(
                "Alpha Quality"
            )

        )



        self.alpha_quality = QSlider(

            Qt.Orientation.Horizontal

        )


        self.alpha_quality.setRange(

            0,

            100

        )


        self.alpha_quality.setValue(

            100

        )


        self.add_widget(

            self.alpha_quality

        )







        # =====================
        # NEAR LOSSLESS
        # =====================


        self.near_lossless = QCheckBox(

            "Near Lossless"

        )


        self.near_lossless.setChecked(

            False

        )


        self.add_widget(

            self.near_lossless

        )







        # =====================
        # EXACT
        # =====================


        self.exact = QCheckBox(

            "Preserve Exact RGB"

        )


        self.exact.setChecked(

            False

        )


        self.add_widget(

            self.exact

        )









    def get_settings(
        self
    ):


        return {


            "lossless":

                self.lossless.isChecked(),



            "quality":

                self.quality.value(),



            "method":

                int(

                    self.method.currentText()

                ),



            "alpha_quality":

                self.alpha_quality.value(),



            "near_lossless":

                self.near_lossless.isChecked(),



            "exact":

                self.exact.isChecked()

        }









    def reset(
        self
    ):


        self.lossless.setChecked(

            False

        )


        self.quality.setValue(

            85

        )


        self.method.setCurrentText(

            "4"

        )


        self.alpha_quality.setValue(

            100

        )


        self.near_lossless.setChecked(

            False

        )


        self.exact.setChecked(

            False

        )