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





class CompressPage(QWidget):



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
            10
        )



        layout.addWidget(

            QLabel(
                "Compress Image"
            )

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
                "Compression Method"
            )

        )



        self.method_box = QComboBox()


        self.method_box.addItems(

            [

                "none",

                "optimize",

                "remove_alpha"

            ]

        )


        layout.addWidget(
            self.method_box
        )






        process_button = QPushButton(
            "Compress"
        )


        process_button.clicked.connect(
            self.compress
        )


        layout.addWidget(
            process_button
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

            "Select Image",

            "",

            (
                "Images "
                "(*.jpg *.jpeg *.png *.webp *.avif "
                "*.gif *.bmp *.tiff *.tif *.heic *.ico)"
            )

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








    def get_output_folder(
        self
    ):


        config_file = Path(

            "config/app_settings.json"

        )



        if config_file.exists():


            try:


                with open(

                    config_file,

                    "r",

                    encoding="utf-8"

                ) as file:


                    data = json.load(file)


                    folder = data.get(

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









    def compress(
        self
    ):


        if not self.selected_file:


            QMessageBox.warning(

                self,

                "Warning",

                "Select image first"

            )


            return






        operation = {


            "type":

                "compression",


            "method":

                self.method_box.currentText()

        }







        output_folder = self.get_output_folder()


        output_folder.mkdir(

            parents=True,

            exist_ok=True

        )



        output_path = output_folder / (

            self.selected_file.stem

            +

            "_compressed"

            +

            self.selected_file.suffix

        )







        config = {


            "operations":

                [

                    operation

                ],



            "output":

                {


                    "format":

                        self.selected_file.suffix.replace(

                            ".",

                            ""

                        ).upper()

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

                "Compression Error",

                str(error)

            )