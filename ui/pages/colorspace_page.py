from pathlib import Path


from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QComboBox,
    QMessageBox
)




class ColorSpacePage(QWidget):


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
                "Color Space"
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
                "Target Color Space"
            )
        )


        self.colorspace_box = QComboBox()


        self.colorspace_box.addItems(
            [
                "sRGB",
                "grayscale",
                "CMYK",
                "Adobe RGB",
                "Display P3"
            ]
        )


        layout.addWidget(
            self.colorspace_box
        )



        layout.addWidget(
            QLabel(
                "Output Format"
            )
        )


        self.format_box = QComboBox()


        self.format_box.addItems(
            [
                "JPEG",
                "PNG",
                "WEBP"
            ]
        )


        layout.addWidget(
            self.format_box
        )



        process = QPushButton(
            "Convert Color Space"
        )


        process.clicked.connect(
            self.convert_colorspace
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



    def convert_colorspace(
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
            "test_data/output/ui_colorspace"
        ) / (

            self.selected_file.stem

            +

            "."

            +

            output_format.lower()

        )



        operation = {

            "type":"colorspace",

            "target":
                self.colorspace_box.currentText()

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