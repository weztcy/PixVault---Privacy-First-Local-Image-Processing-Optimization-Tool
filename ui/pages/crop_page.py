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
    QMessageBox
)




class CropPage(QWidget):


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
                "Crop"
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
                "Crop Mode"
            )
        )


        self.mode_box = QComboBox()


        self.mode_box.addItems(
            [
                "fixed",
                "percentage",
                "coordinates",
                "aspect_ratio"
            ]
        )


        layout.addWidget(
            self.mode_box
        )



        layout.addWidget(
            QLabel(
                "Width"
            )
        )


        self.width_spin = QSpinBox()


        self.width_spin.setRange(
            1,
            10000
        )


        self.width_spin.setValue(
            500
        )


        layout.addWidget(
            self.width_spin
        )



        layout.addWidget(
            QLabel(
                "Height"
            )
        )


        self.height_spin = QSpinBox()


        self.height_spin.setRange(
            1,
            10000
        )


        self.height_spin.setValue(
            500
        )


        layout.addWidget(
            self.height_spin
        )



        layout.addWidget(
            QLabel(
                "Percentage (%)"
            )
        )


        self.percent_spin = QSpinBox()


        self.percent_spin.setRange(
            1,
            100
        )


        self.percent_spin.setValue(
            50
        )


        layout.addWidget(
            self.percent_spin
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
            "Crop"
        )


        process.clicked.connect(
            self.crop_image
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



    def crop_image(
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
            "test_data/output/ui_crop"
        ) / (

            self.selected_file.stem

            +

            "."

            +

            output_format.lower()

        )



        mode = self.mode_box.currentText()



        operation = {

            "type":"crop",

            "mode":mode

        }



        if mode == "fixed":

            operation.update({

                "width":
                    self.width_spin.value(),

                "height":
                    self.height_spin.value()

            })



        elif mode == "percentage":

            operation.update({

                "value":
                    self.percent_spin.value()

            })



        elif mode == "aspect_ratio":

            operation.update({

                "width":
                    self.width_spin.value(),

                "height":
                    self.height_spin.value()

            })



        elif mode == "coordinates":

            operation.update({

                "x":0,

                "y":0,

                "width":
                    self.width_spin.value(),

                "height":
                    self.height_spin.value()

            })



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