from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QSpinBox,
    QCheckBox,
    QGroupBox
)




class EncoderOptionsPanel(QWidget):


    def __init__(
        self
    ):

        super().__init__()


        self.current_widgets = {}


        self.setup_ui()



    def setup_ui(
        self
    ):


        layout = QVBoxLayout()



        self.format_box = QComboBox()


        self.format_box.addItems(
            [
                "WEBP",
                "JPEG",
                "PNG",
                "AVIF",
                "TIFF",
                "BMP",
                "GIF",
                "ICO"
            ]
        )


        self.format_box.currentTextChanged.connect(
            self.change_options
        )



        layout.addWidget(
            QLabel(
                "Output Format"
            )
        )


        layout.addWidget(
            self.format_box
        )



        self.options_box = QGroupBox(
            "Format Options"
        )


        self.options_layout = QVBoxLayout()


        self.options_box.setLayout(
            self.options_layout
        )


        layout.addWidget(
            self.options_box
        )


        self.setLayout(
            layout
        )


        self.change_options(
            "WEBP"
        )



    def clear_options(
        self
    ):


        while self.options_layout.count():


            item = self.options_layout.takeAt(
                0
            )


            widget = item.widget()


            if widget:

                widget.deleteLater()



        self.current_widgets.clear()



    def change_options(
        self,
        format_name
    ):


        self.clear_options()



        if format_name == "WEBP":

            self.webp_options()


        elif format_name == "JPEG":

            self.jpeg_options()


        elif format_name == "PNG":

            self.png_options()


        elif format_name == "AVIF":

            self.avif_options()


        elif format_name == "TIFF":

            self.tiff_options()


        elif format_name == "BMP":

            self.bmp_options()


        elif format_name == "GIF":

            self.gif_options()


        elif format_name == "ICO":

            self.ico_options()



    # =====================
    # WEBP
    # =====================


    def webp_options(
        self
    ):


        mode = QComboBox()

        mode.addItems(
            [
                "lossy",
                "lossless"
            ]
        )


        quality = QSpinBox()

        quality.setRange(
            1,
            100
        )

        quality.setValue(
            85
        )


        alpha = QSpinBox()

        alpha.setRange(
            1,
            100
        )

        alpha.setValue(
            90
        )



        self.current_widgets["mode"] = mode

        self.current_widgets["quality"] = quality

        self.current_widgets["alpha_quality"] = alpha



        self.add(
            "Mode",
            mode
        )

        self.add(
            "Quality",
            quality
        )

        self.add(
            "Alpha Quality",
            alpha
        )



    # =====================
    # JPEG
    # =====================


    def jpeg_options(
        self
    ):


        quality = QSpinBox()


        quality.setRange(
            1,
            100
        )


        quality.setValue(
            85
        )


        progressive = QCheckBox(
            "Progressive"
        )


        optimize = QCheckBox(
            "Optimize"
        )


        self.current_widgets["quality"] = quality

        self.current_widgets["progressive"] = progressive

        self.current_widgets["optimize"] = optimize



        self.add(
            "Quality",
            quality
        )


        self.options_layout.addWidget(
            progressive
        )


        self.options_layout.addWidget(
            optimize
        )



    # =====================
    # PNG
    # =====================


    def png_options(
        self
    ):


        compression = QSpinBox()


        compression.setRange(
            0,
            9
        )


        compression.setValue(
            6
        )


        interlace = QCheckBox(
            "Interlace"
        )


        self.current_widgets["compression"] = compression

        self.current_widgets["interlace"] = interlace



        self.add(
            "Compression Level",
            compression
        )


        self.options_layout.addWidget(
            interlace
        )



    # =====================
    # AVIF
    # =====================


    def avif_options(
        self
    ):


        quality = QSpinBox()


        quality.setRange(
            1,
            100
        )


        quality.setValue(
            80
        )


        speed = QSpinBox()


        speed.setRange(
            0,
            10
        )


        speed.setValue(
            5
        )


        self.current_widgets["quality"] = quality

        self.current_widgets["speed"] = speed



        self.add(
            "Quality",
            quality
        )


        self.add(
            "Speed",
            speed
        )



    # =====================
    # TIFF
    # =====================


    def tiff_options(
        self
    ):


        compression = QComboBox()


        compression.addItems(
            [
                "none",
                "lzw",
                "deflate"
            ]
        )


        self.current_widgets["compression"] = compression



        self.add(
            "Compression",
            compression
        )



    # =====================
    # BMP
    # =====================


    def bmp_options(
        self
    ):


        depth = QComboBox()


        depth.addItems(
            [
                "24",
                "32"
            ]
        )


        self.current_widgets["depth"] = depth



        self.add(
            "Bit Depth",
            depth
        )



    # =====================
    # GIF
    # =====================


    def gif_options(
        self
    ):


        colors = QSpinBox()


        colors.setRange(
            2,
            256
        )


        colors.setValue(
            256
        )


        self.current_widgets["colors"] = colors



        self.add(
            "Colors",
            colors
        )



    # =====================
    # ICO
    # =====================


    def ico_options(
        self
    ):


        size = QComboBox()


        size.addItems(
            [
                "16",
                "32",
                "64",
                "128",
                "256"
            ]
        )


        self.current_widgets["size"] = size



        self.add(
            "Icon Size",
            size
        )



    def add(
        self,
        label,
        widget
    ):


        self.options_layout.addWidget(
            QLabel(
                label
            )
        )


        self.options_layout.addWidget(
            widget
        )



    def get_config(
        self
    ):


        config = {

            "format":
                self.format_box.currentText()

        }



        quality = self.current_widgets.get(
            "quality"
        )


        if quality:

            config["quality"] = (
                quality.value()
            )



        compression = self.current_widgets.get(
            "compression"
        )


        if compression:


            if isinstance(
                compression,
                QSpinBox
            ):

                config["compression"] = (
                    compression.value()
                )


            else:

                config["compression"] = (
                    compression.currentText()
                )



        speed = self.current_widgets.get(
            "speed"
        )


        if speed:

            config["speed"] = (
                speed.value()
            )



        return config