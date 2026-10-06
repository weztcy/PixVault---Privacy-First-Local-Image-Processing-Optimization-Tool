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





class HEICOptions(
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

            85

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

                "hevc",

                "hevc_lossless"

            ]

        )


        self.compression.setCurrentText(

            "hevc"

        )


        self.add_widget(

            self.compression

        )









        # =====================
        # CHROMA
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

                "4:2:0"

            ]

        )


        self.subsampling.setCurrentText(

            "4:2:0"

        )


        self.add_widget(

            self.subsampling

        )









        # =====================
        # METADATA
        # =====================


        self.preserve_metadata = QCheckBox(

            "Preserve Metadata"

        )


        self.preserve_metadata.setChecked(

            False

        )


        self.add_widget(

            self.preserve_metadata

        )









        # =====================
        # ALPHA
        # =====================


        self.alpha = QCheckBox(

            "Enable Alpha Channel"

        )


        self.alpha.setChecked(

            True

        )


        self.add_widget(

            self.alpha

        )









    def get_settings(
        self
    ):


        return {


            "quality":

                self.quality.value(),



            "lossless":

                self.lossless.isChecked(),



            "compression":

                self.compression.currentText(),



            "subsampling":

                self.subsampling.currentText(),



            "preserve_metadata":

                self.preserve_metadata.isChecked(),



            "alpha":

                self.alpha.isChecked()

        }









    def reset(
        self
    ):


        self.quality.setValue(

            85

        )


        self.lossless.setChecked(

            False

        )


        self.compression.setCurrentText(

            "hevc"

        )


        self.subsampling.setCurrentText(

            "4:2:0"

        )


        self.preserve_metadata.setChecked(

            False

        )


        self.alpha.setChecked(

            True

        )