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





class JPEGOptions(
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
        # PROGRESSIVE
        # =====================


        self.progressive = QCheckBox(

            "Progressive JPEG"

        )


        self.progressive.setChecked(

            True

        )


        self.add_widget(

            self.progressive

        )







        # =====================
        # OPTIMIZE
        # =====================


        self.optimize = QCheckBox(

            "Optimize Huffman Coding"

        )


        self.optimize.setChecked(

            True

        )


        self.add_widget(

            self.optimize

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

                "4:2:0"

            ]

        )



        self.subsampling.setCurrentText(

            "4:2:0"

        )



        self.add_widget(

            self.subsampling

        )









    def get_settings(
        self
    ):


        return {


            "quality":

                self.quality.value(),



            "progressive":

                self.progressive.isChecked(),



            "optimize":

                self.optimize.isChecked(),



            "subsampling":

                self.subsampling.currentText()

        }







    def reset(
        self
    ):


        self.quality.setValue(

            85

        )


        self.progressive.setChecked(

            True

        )


        self.optimize.setChecked(

            True

        )


        self.subsampling.setCurrentText(

            "4:2:0"

        )