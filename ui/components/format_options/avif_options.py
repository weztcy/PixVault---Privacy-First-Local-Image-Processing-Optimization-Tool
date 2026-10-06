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





class AVIFOptions(
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

            80

        )


        self.add_widget(

            self.quality

        )








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
        # SPEED
        # =====================


        self.add_widget(

            QLabel(
                "Encoder Speed"
            )

        )


        self.speed = QSlider(

            Qt.Orientation.Horizontal

        )


        self.speed.setRange(

            0,

            10

        )


        self.speed.setValue(

            6

        )


        self.add_widget(

            self.speed

        )








        # =====================
        # SUBSAMPLING
        # =====================


        self.add_widget(

            QLabel(
                "Chroma Subsampling"
            )

        )



        self.subsampling = QComboBox()



        self.subsampling.addItems(

            [

                "4:4:4",

                "4:2:2",

                "4:2:0",

                "monochrome"

            ]

        )



        self.subsampling.setCurrentText(

            "4:2:0"

        )


        self.add_widget(

            self.subsampling

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
        # PROGRESSIVE
        # =====================


        self.progressive = QCheckBox(

            "Progressive Encoding"

        )


        self.progressive.setChecked(

            False

        )


        self.add_widget(

            self.progressive

        )









    def get_settings(
        self
    ):


        return {


            "quality":

                self.quality.value(),



            "lossless":

                self.lossless.isChecked(),



            "speed":

                self.speed.value(),



            "subsampling":

                self.subsampling.currentText(),



            "alpha_quality":

                self.alpha_quality.value(),



            "progressive":

                self.progressive.isChecked()

        }








    def reset(
        self
    ):


        self.quality.setValue(

            80

        )


        self.lossless.setChecked(

            False

        )


        self.speed.setValue(

            6

        )


        self.subsampling.setCurrentText(

            "4:2:0"

        )


        self.alpha_quality.setValue(

            100

        )


        self.progressive.setChecked(

            False

        )