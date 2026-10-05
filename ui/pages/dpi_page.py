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




class DPIPage(QWidget):


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
                "DPI Processor"
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
                "Unit"
            )
        )



        self.unit_box = QComboBox()


        self.unit_box.addItems(
            [
                "dpi",
                "dpcm"
            ]
        )


        layout.addWidget(
            self.unit_box
        )



        layout.addWidget(
            QLabel(
                "Horizontal DPI"
            )
        )


        self.horizontal_spin = QSpinBox()


        self.horizontal_spin.setRange(
            1,
            5000
        )


        self.horizontal_spin.setValue(
            300
        )


        layout.addWidget(
            self.horizontal_spin
        )



        layout.addWidget(
            QLabel(
                "Vertical DPI"
            )
        )


        self.vertical_spin = QSpinBox()


        self.vertical_spin.setRange(
            1,
            5000
        )


        self.vertical_spin.setValue(
            300
        )


        layout.addWidget(
            self.vertical_spin
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
            "Change DPI"
        )


        process.clicked.connect(
            self.change_dpi
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



    def change_dpi(
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
            "test_data/output/ui_dpi"
        ) / (

            self.selected_file.stem

            +

            "."

            +

            output_format.lower()

        )



        operation = {

            "type":"dpi",

            "unit":
                self.unit_box.currentText(),

            "horizontal":
                self.horizontal_spin.value(),

            "vertical":
                self.vertical_spin.value()

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