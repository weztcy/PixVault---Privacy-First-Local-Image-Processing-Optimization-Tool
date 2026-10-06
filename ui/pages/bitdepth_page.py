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





class BitDepthPage(QWidget):



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
                "Bit Depth Processor"
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
                "Target Bit Depth"
            )

        )



        self.depth_box = QComboBox()


        self.depth_box.addItems(

            [

                "8",

                "16",

                "32"

            ]

        )


        layout.addWidget(
            self.depth_box
        )







        process = QPushButton(

            "Apply Bit Depth"

        )


        process.clicked.connect(

            self.convert_bitdepth

        )


        layout.addWidget(
            process
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








    def convert_bitdepth(
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

                "bitdepth",



            "value":

                int(

                    self.depth_box.currentText()

                )

        }







        output_folder = self.get_output_folder()


        output_folder.mkdir(

            parents=True,

            exist_ok=True

        )



        output_path = output_folder / (

            self.selected_file.stem

            +

            "_bitdepth"

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

                "Bit Depth Error",

                str(error)

            )