from pathlib import Path


from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QCheckBox,
    QMessageBox
)




class ResizePage(QWidget):


    def __init__(
        self,
        image_service
    ):

        super().__init__()


        self.image_service = image_service


        self.selected_file = None


        self.setup_ui()



    def setup_ui(
        self
    ):


        layout = QVBoxLayout()



        layout.addWidget(
            QLabel(
                "Resize"
            )
        )



        self.file_input = QLineEdit()

        self.file_input.setReadOnly(
            True
        )


        browse = QPushButton(
            "Select Image"
        )


        browse.clicked.connect(
            self.select_file
        )


        layout.addWidget(
            self.file_input
        )


        layout.addWidget(
            browse
        )



        layout.addWidget(
            QLabel(
                "Resize Method"
            )
        )


        self.method_box = QComboBox()


        self.method_box.addItems(
            [
                "exact",
                "width",
                "height",
                "percentage"
            ]
        )


        layout.addWidget(
            self.method_box
        )



        layout.addWidget(
            QLabel(
                "Value"
            )
        )


        self.value_spin = QSpinBox()


        self.value_spin.setRange(
            1,
            10000
        )


        self.value_spin.setValue(
            800
        )


        layout.addWidget(
            self.value_spin
        )



        self.keep_ratio = QCheckBox(
            "Keep Aspect Ratio"
        )


        self.keep_ratio.setChecked(
            True
        )


        layout.addWidget(
            self.keep_ratio
        )



        layout.addWidget(
            QLabel(
                "Resampling"
            )
        )


        self.resampling_box = QComboBox()


        self.resampling_box.addItems(
            [
                "lanczos",
                "bicubic",
                "bilinear",
                "nearest"
            ]
        )


        layout.addWidget(
            self.resampling_box
        )



        layout.addWidget(
            QLabel(
                "Output Format"
            )
        )


        self.format_box = QComboBox()


        self.format_box.addItems(
            [
                "WEBP",
                "JPEG",
                "PNG"
            ]
        )


        layout.addWidget(
            self.format_box
        )



        process = QPushButton(
            "Resize"
        )


        process.clicked.connect(
            self.resize_image
        )


        layout.addWidget(
            process
        )



        self.result_label = QLabel()


        layout.addWidget(
            self.result_label
        )



        self.setLayout(
            layout
        )



    def select_file(
        self
    ):


        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image"
        )


        if file:

            self.selected_file = Path(
                file
            )


            self.file_input.setText(
                str(
                    self.selected_file
                )
            )



    def resize_image(
        self
    ):


        if not self.selected_file:


            QMessageBox.warning(
                self,
                "Warning",
                "Select image first"
            )


            return



        output_format = self.format_box.currentText()


        output_path = Path(
            "test_data/output/ui_resize"
        ) / (

            self.selected_file.stem

            +

            "."

            +

            output_format.lower()

        )



        method = self.method_box.currentText()



        operation = {

            "type":"resize",

            "method":method,

            "value":
                self.value_spin.value(),

            "keep_aspect_ratio":
                self.keep_ratio.isChecked(),

            "resampling":
                self.resampling_box.currentText()

        }



        config = {

            "operations":[
                operation
            ],

            "output":{

                "format":
                    output_format,

                "quality":85

            }

        }



        try:


            result = self.image_service.process_image(

                self.selected_file,

                output_path,

                config

            )


            self.result_label.setText(
                f"Completed:\n{result}"
            )



        except Exception as error:


            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )