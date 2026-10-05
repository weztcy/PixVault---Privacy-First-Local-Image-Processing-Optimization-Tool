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




class MetadataPage(QWidget):


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
                "Metadata"
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



        remove_button = QPushButton(
            "Remove Metadata"
        )


        remove_button.clicked.connect(
            self.remove_metadata
        )


        layout.addWidget(
            remove_button
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



    def remove_metadata(
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
            "test_data/output/ui_metadata"
        ) / (

            self.selected_file.stem

            +

            "."

            +

            output_format.lower()

        )



        operation = {

            "type":"metadata",

            "mode":"all"

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