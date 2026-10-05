from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QPushButton,
    QGroupBox,
    QLabel,
    QComboBox,
    QSpinBox
)




class ProcessingPanel(QWidget):


    def __init__(
        self
    ):

        super().__init__()


        self.operations = {}


        self.setup_ui()



    def setup_ui(
        self
    ):


        layout = QVBoxLayout()


        self.add_resize_section(
            layout
        )


        self.add_crop_section(
            layout
        )


        self.add_transform_section(
            layout
        )


        self.add_compression_section(
            layout
        )


        self.add_dpi_section(
            layout
        )


        self.add_colorspace_section(
            layout
        )


        self.add_bitdepth_section(
            layout
        )


        self.add_metadata_section(
            layout
        )


        layout.addStretch()


        self.setLayout(
            layout
        )



    def create_section(
        self,
        title,
        key,
        content
    ):


        box = QGroupBox()


        layout = QVBoxLayout()



        header = QHBoxLayout()



        checkbox = QCheckBox(
            title
        )


        expand_button = QPushButton(
            "▼"
        )


        expand_button.setFixedWidth(
            30
        )


        header.addWidget(
            checkbox
        )


        header.addStretch()


        header.addWidget(
            expand_button
        )



        layout.addLayout(
            header
        )


        layout.addWidget(
            content
        )


        content.hide()



        expand_button.clicked.connect(

            lambda:

            content.setVisible(
                not content.isVisible()
            )

        )


        box.setLayout(
            layout
        )


        self.operations[key] = {

            "checkbox": checkbox,

            "widget": content

        }


        return box



    # ==========================
    # RESIZE
    # ==========================


    def add_resize_section(
        self,
        layout
    ):


        widget = QWidget()


        form = QVBoxLayout()



        self.resize_method = QComboBox()


        self.resize_method.addItems(
            [
                "width",
                "height",
                "percentage",
                "longest_side"
            ]
        )



        self.resize_value = QSpinBox()


        self.resize_value.setRange(
            1,
            10000
        )


        self.resize_value.setValue(
            1920
        )



        self.keep_ratio = QCheckBox(
            "Keep Aspect Ratio"
        )


        self.keep_ratio.setChecked(
            True
        )



        form.addWidget(
            QLabel(
                "Method"
            )
        )


        form.addWidget(
            self.resize_method
        )


        form.addWidget(
            QLabel(
                "Value"
            )
        )


        form.addWidget(
            self.resize_value
        )


        form.addWidget(
            self.keep_ratio
        )


        widget.setLayout(
            form
        )


        layout.addWidget(

            self.create_section(

                "Resize",

                "resize",

                widget

            )

        )



    # ==========================
    # CROP
    # ==========================


    def add_crop_section(
        self,
        layout
    ):


        widget = QWidget()


        form = QVBoxLayout()



        self.crop_mode = QComboBox()


        self.crop_mode.addItems(
            [
                "aspect_ratio",
                "fixed",
                "percentage"
            ]
        )



        self.crop_ratio = QComboBox()


        self.crop_ratio.addItems(
            [
                "16:9",
                "4:3",
                "1:1"
            ]
        )



        form.addWidget(
            QLabel(
                "Mode"
            )
        )


        form.addWidget(
            self.crop_mode
        )


        form.addWidget(
            QLabel(
                "Ratio"
            )
        )


        form.addWidget(
            self.crop_ratio
        )


        widget.setLayout(
            form
        )


        layout.addWidget(

            self.create_section(

                "Crop",

                "crop",

                widget

            )

        )



    # ==========================
    # TRANSFORM
    # ==========================


    def add_transform_section(
        self,
        layout
    ):


        widget = QWidget()


        form = QVBoxLayout()



        self.rotation = QComboBox()


        self.rotation.addItems(
            [
                "none",
                "90",
                "180",
                "270"
            ]
        )



        self.flip = QComboBox()


        self.flip.addItems(
            [
                "none",
                "horizontal",
                "vertical",
                "both"
            ]
        )



        form.addWidget(
            QLabel(
                "Rotation"
            )
        )


        form.addWidget(
            self.rotation
        )


        form.addWidget(
            QLabel(
                "Flip"
            )
        )


        form.addWidget(
            self.flip
        )



        widget.setLayout(
            form
        )


        layout.addWidget(

            self.create_section(

                "Transform",

                "transform",

                widget

            )

        )



    # ==========================
    # COMPRESSION
    # ==========================


    def add_compression_section(
        self,
        layout
    ):


        widget = QWidget()


        form = QVBoxLayout()



        self.compression_quality = QSpinBox()


        self.compression_quality.setRange(
            1,
            100
        )


        self.compression_quality.setValue(
            85
        )



        form.addWidget(
            QLabel(
                "Quality"
            )
        )


        form.addWidget(
            self.compression_quality
        )



        widget.setLayout(
            form
        )


        layout.addWidget(

            self.create_section(

                "Compression",

                "compression",

                widget

            )

        )



    # ==========================
    # DPI
    # ==========================


    def add_dpi_section(
        self,
        layout
    ):


        widget = QWidget()


        form = QVBoxLayout()



        self.dpi_value = QSpinBox()


        self.dpi_value.setRange(
            72,
            1200
        )


        self.dpi_value.setValue(
            300
        )



        form.addWidget(
            QLabel(
                "DPI"
            )
        )


        form.addWidget(
            self.dpi_value
        )


        widget.setLayout(
            form
        )


        layout.addWidget(

            self.create_section(

                "DPI / Resolution",

                "dpi",

                widget

            )

        )



    # ==========================
    # COLOR SPACE
    # ==========================


    def add_colorspace_section(
        self,
        layout
    ):


        widget = QWidget()


        form = QVBoxLayout()



        self.color_space = QComboBox()


        self.color_space.addItems(
            [
                "sRGB",
                "Adobe RGB",
                "Display P3",
                "CMYK",
                "Grayscale"
            ]
        )


        form.addWidget(
            self.color_space
        )


        widget.setLayout(
            form
        )


        layout.addWidget(

            self.create_section(

                "Color Space",

                "colorspace",

                widget

            )

        )



    # ==========================
    # BIT DEPTH
    # ==========================


    def add_bitdepth_section(
        self,
        layout
    ):


        widget = QWidget()


        form = QVBoxLayout()



        self.bit_depth = QComboBox()


        self.bit_depth.addItems(
            [
                "8",
                "16",
                "32"
            ]
        )


        form.addWidget(
            self.bit_depth
        )


        widget.setLayout(
            form
        )


        layout.addWidget(

            self.create_section(

                "Bit Depth",

                "bitdepth",

                widget

            )

        )



    # ==========================
    # METADATA
    # ==========================


    def add_metadata_section(
        self,
        layout
    ):


        widget = QWidget()


        form = QVBoxLayout()


        self.metadata_mode = QComboBox()


        self.metadata_mode.addItems(
            [
                "all",
                "custom"
            ]
        )


        form.addWidget(
            QLabel(
                "Mode"
            )
        )


        form.addWidget(
            self.metadata_mode
        )


        widget.setLayout(
            form
        )


        layout.addWidget(

            self.create_section(

                "Remove Metadata",

                "metadata",

                widget

            )

        )



    # ==========================
    # CONFIG GENERATOR
    # ==========================


    def get_operations(
        self
    ):


        result = []



        if self.operations["resize"]["checkbox"].isChecked():

            result.append(
                {
                    "type":"resize",

                    "method":
                        self.resize_method.currentText(),

                    "value":
                        self.resize_value.value(),

                    "keep_ratio":
                        self.keep_ratio.isChecked()
                }
            )



        if self.operations["crop"]["checkbox"].isChecked():

            result.append(
                {
                    "type":"crop",

                    "mode":
                        self.crop_mode.currentText(),

                    "ratio":
                        self.crop_ratio.currentText()
                }
            )



        if self.operations["transform"]["checkbox"].isChecked():

            result.append(
                {
                    "type":"transform",

                    "rotation":
                        self.rotation.currentText(),

                    "flip":
                        self.flip.currentText()
                }
            )



        if self.operations["compression"]["checkbox"].isChecked():

            result.append(
                {
                    "type":"compression",

                    "quality":
                        self.compression_quality.value()
                }
            )



        if self.operations["dpi"]["checkbox"].isChecked():

            result.append(
                {
                    "type":"dpi",

                    "value":
                        self.dpi_value.value()
                }
            )



        if self.operations["colorspace"]["checkbox"].isChecked():

            result.append(
                {
                    "type":"colorspace",

                    "target":
                        self.color_space.currentText()
                }
            )



        if self.operations["bitdepth"]["checkbox"].isChecked():

            result.append(
                {
                    "type":"bitdepth",

                    "value":
                        int(
                            self.bit_depth.currentText()
                        )
                }
            )



        if self.operations["metadata"]["checkbox"].isChecked():

            result.append(
                {
                    "type":"metadata",

                    "mode":
                        self.metadata_mode.currentText()
                }
            )



        return result