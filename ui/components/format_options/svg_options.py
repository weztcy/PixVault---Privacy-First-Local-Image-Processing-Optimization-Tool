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





class SVGOptions(
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
        # SVG VERSION
        # =====================


        self.add_widget(

            QLabel(
                "SVG Version"
            )

        )


        self.version = QComboBox()



        self.version.addItems(

            [

                "1.0",

                "1.1",

                "2.0"

            ]

        )


        self.version.setCurrentText(

            "1.1"

        )


        self.add_widget(

            self.version

        )








        # =====================
        # PRECISION
        # =====================


        self.add_widget(

            QLabel(
                "Decimal Precision"
            )

        )


        self.precision = QSlider(

            Qt.Orientation.Horizontal

        )


        self.precision.setRange(

            0,

            10

        )


        self.precision.setValue(

            3

        )


        self.add_widget(

            self.precision

        )








        # =====================
        # OPTIMIZE PATH
        # =====================


        self.optimize_path = QCheckBox(

            "Optimize SVG Paths"

        )


        self.optimize_path.setChecked(

            True

        )


        self.add_widget(

            self.optimize_path

        )








        # =====================
        # REMOVE METADATA
        # =====================


        self.remove_metadata = QCheckBox(

            "Remove Metadata"

        )


        self.remove_metadata.setChecked(

            True

        )


        self.add_widget(

            self.remove_metadata

        )








        # =====================
        # EMBED IMAGES
        # =====================


        self.embed_images = QCheckBox(

            "Embed Raster Images"

        )


        self.embed_images.setChecked(

            False

        )


        self.add_widget(

            self.embed_images

        )








        # =====================
        # TEXT AS PATH
        # =====================


        self.text_as_path = QCheckBox(

            "Convert Text To Path"

        )


        self.text_as_path.setChecked(

            False

        )


        self.add_widget(

            self.text_as_path

        )









    def get_settings(
        self
    ):


        return {


            "version":

                self.version.currentText(),



            "precision":

                self.precision.value(),



            "optimize_path":

                self.optimize_path.isChecked(),



            "remove_metadata":

                self.remove_metadata.isChecked(),



            "embed_images":

                self.embed_images.isChecked(),



            "text_as_path":

                self.text_as_path.isChecked()

        }









    def reset(
        self
    ):


        self.version.setCurrentText(

            "1.1"

        )


        self.precision.setValue(

            3

        )


        self.optimize_path.setChecked(

            True

        )


        self.remove_metadata.setChecked(

            True

        )


        self.embed_images.setChecked(

            False

        )


        self.text_as_path.setChecked(

            False

        )