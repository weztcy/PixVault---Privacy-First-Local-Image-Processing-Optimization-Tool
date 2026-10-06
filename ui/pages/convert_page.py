from pathlib import Path
import json


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



class ConvertPage(QWidget):


    def __init__(
        self,
        image_service,
        batch_service=None
    ):

        super().__init__()


        self.image_service = image_service

        self.batch_service = batch_service


        self.selected_file = None


        self.setup_ui()



    def setup_ui(
        self
    ):


        layout = QVBoxLayout()


        layout.setSpacing(
            12
        )



        title = QLabel(
            "Convert Image"
        )


        layout.addWidget(
            title
        )



        self.file_input = QLineEdit()


        self.file_input.setReadOnly(
            True
        )



        browse_button = QPushButton(
            "Select Image"
        )


        browse_button.clicked.connect(
            self.select_file
        )



        layout.addWidget(
            self.file_input
        )


        layout.addWidget(
            browse_button
        )



        layout.addWidget(
            QLabel(
                "Target Format"
            )
        )



        self.format_box = QComboBox()



        self.format_box.addItems(

            [

                "JPEG",

                "PNG",

                "WEBP",

                "AVIF",

                "GIF",

                "BMP",

                "TIFF",

                "HEIC",

                "HEIF",

                "ICO",

                "SVG"

            ]

        )



        layout.addWidget(
            self.format_box
        )



        self.output_info = QLabel()


        layout.addWidget(
            self.output_info
        )



        convert_button = QPushButton(
            "Convert"
        )


        convert_button.clicked.connect(
            self.convert
        )


        layout.addWidget(
            convert_button
        )



        self.result_label = QLabel()


        layout.addWidget(
            self.result_label
        )


        layout.addStretch()



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



            self.update_info()







    def update_info(
        self
    ):


        if not self.selected_file:

            return



        self.output_info.setText(

            f"Input:\n{self.selected_file.name}\n\n"
            f"Output format:\n{self.format_box.currentText()}"

        )






    def get_output_folder(
        self
    ):


        settings_file = Path(

            "config/app_settings.json"

        )



        if settings_file.exists():

            try:


                with open(

                    settings_file,

                    "r",

                    encoding="utf-8"

                ) as file:


                    settings = json.load(
                        file
                    )


                    folder = settings.get(

                        "output_folder"

                    )


                    if folder:


                        return Path(
                            folder
                        )


            except Exception:

                pass



        return Path(
            "output"
        )







    def convert(
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



        output_folder = self.get_output_folder()



        output_folder.mkdir(

            parents=True,

            exist_ok=True

        )



        output_path = output_folder / (

            self.selected_file.stem

            +

            "."

            +

            output_format.lower()

        )






        config = {


            "operations": [],


            "output": {


                "format":

                    output_format,


                "quality":

                    85

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

                "Conversion Error",

                str(error)

            )