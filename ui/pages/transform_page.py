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




class TransformPage(QWidget):


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
                "Transform"
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
                "Operation"
            )
        )


        self.operation_box = QComboBox()


        self.operation_box.addItems(
            [
                "rotate",
                "flip_horizontal",
                "flip_vertical",
                "flip_both"
            ]
        )


        layout.addWidget(
            self.operation_box
        )



        layout.addWidget(
            QLabel(
                "Rotation Angle"
            )
        )


        self.angle_spin = QSpinBox()


        self.angle_spin.setRange(
            -360,
            360
        )


        self.angle_spin.setValue(
            90
        )


        layout.addWidget(
            self.angle_spin
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
            "Transform"
        )


        process.clicked.connect(
            self.transform_image
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



    def transform_image(
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
            "test_data/output/ui_transform"
        ) / (

            self.selected_file.stem

            +

            "."

            +

            output_format.lower()

        )



        operation_name = self.operation_box.currentText()



        operation = {

            "type":"transform"

        }



        if operation_name == "rotate":

            operation.update({

                "operation":"rotate",

                "angle":
                    self.angle_spin.value()

            })



        elif operation_name == "flip_horizontal":

            operation.update({

                "operation":"flip",

                "direction":"horizontal"

            })



        elif operation_name == "flip_vertical":

            operation.update({

                "operation":"flip",

                "direction":"vertical"

            })



        elif operation_name == "flip_both":

            operation.update({

                "operation":"flip",

                "direction":"both"

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