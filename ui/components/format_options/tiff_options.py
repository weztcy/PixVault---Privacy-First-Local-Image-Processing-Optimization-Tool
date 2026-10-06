from PySide6.QtWidgets import (
    QLabel,
    QCheckBox,
    QComboBox,
    QLineEdit
)


from ui.components.format_options.base_format_options import (
    BaseFormatOptions
)





class TIFFOptions(
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

                "lzw",

                "deflate",

                "packbits",

                "jpeg",

                "zstd"

            ]

        )


        self.compression.setCurrentText(

            "lzw"

        )


        self.add_widget(

            self.compression

        )








        # =====================
        # PREDICTOR
        # =====================


        self.add_widget(

            QLabel(
                "Predictor"
            )

        )


        self.predictor = QComboBox()



        self.predictor.addItems(

            [

                "none",

                "horizontal",

                "floating_point"

            ]

        )


        self.predictor.setCurrentText(

            "horizontal"

        )


        self.add_widget(

            self.predictor

        )








        # =====================
        # BIG TIFF
        # =====================


        self.bigtiff = QCheckBox(

            "Enable BigTIFF"

        )


        self.bigtiff.setChecked(

            False

        )


        self.add_widget(

            self.bigtiff

        )








        # =====================
        # TILED
        # =====================


        self.tiled = QCheckBox(

            "Enable Tiled Image"

        )


        self.tiled.setChecked(

            False

        )


        self.add_widget(

            self.tiled

        )








        # =====================
        # TILE WIDTH
        # =====================


        self.add_widget(

            QLabel(
                "Tile Width"
            )

        )


        self.tile_width = QLineEdit(

            "256"

        )


        self.add_widget(

            self.tile_width

        )








        # =====================
        # TILE HEIGHT
        # =====================


        self.add_widget(

            QLabel(
                "Tile Height"
            )

        )


        self.tile_height = QLineEdit(

            "256"

        )


        self.add_widget(

            self.tile_height

        )








        # =====================
        # DPI
        # =====================


        self.add_widget(

            QLabel(
                "Resolution DPI"
            )

        )


        self.dpi = QLineEdit(

            "300"

        )


        self.add_widget(

            self.dpi

        )









    def get_settings(
        self
    ):


        return {


            "compression":

                self.compression.currentText(),



            "predictor":

                self.predictor.currentText(),



            "bigtiff":

                self.bigtiff.isChecked(),



            "tiled":

                self.tiled.isChecked(),



            "tile_width":

                self.tile_width.text(),



            "tile_height":

                self.tile_height.text(),



            "dpi":

                self.dpi.text()

        }









    def reset(
        self
    ):


        self.compression.setCurrentText(

            "lzw"

        )


        self.predictor.setCurrentText(

            "horizontal"

        )


        self.bigtiff.setChecked(

            False

        )


        self.tiled.setChecked(

            False

        )


        self.tile_width.setText(

            "256"

        )


        self.tile_height.setText(

            "256"

        )


        self.dpi.setText(

            "300"

        )