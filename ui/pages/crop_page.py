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
    QSpinBox,
    QMessageBox
)





class CropPage(QWidget):



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
                "Crop Image"
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

                "aspect_ratio",

                "coordinates"

            ]

        )


        self.mode_box.currentTextChanged.connect(

            self.update_mode

        )


        layout.addWidget(

            self.mode_box

        )







        self.width_spin = QSpinBox()


        self.width_spin.setRange(

            1,

            100000

        )


        self.width_spin.setValue(

            500

        )



        self.height_spin = QSpinBox()


        self.height_spin.setRange(

            1,

            100000

        )


        self.height_spin.setValue(

            500

        )



        self.percent_spin = QSpinBox()


        self.percent_spin.setRange(

            1,

            100

        )


        self.percent_spin.setValue(

            50

        )



        self.ratio_box = QComboBox()


        self.ratio_box.addItems(

            [

                "1:1",

                "4:3",

                "16:9",

                "3:2",

                "9:16"

            ]

        )





        self.x_spin = QSpinBox()


        self.x_spin.setRange(

            0,

            100000

        )


        self.y_spin = QSpinBox()


        self.y_spin.setRange(

            0,

            100000

        )



        layout.addWidget(

            QLabel(
                "Width"
            )

        )

        layout.addWidget(

            self.width_spin

        )



        layout.addWidget(

            QLabel(
                "Height"
            )

        )

        layout.addWidget(

            self.height_spin

        )



        layout.addWidget(

            QLabel(
                "Percentage"
            )

        )

        layout.addWidget(

            self.percent_spin

        )



        layout.addWidget(

            QLabel(
                "Aspect Ratio"
            )

        )

        layout.addWidget(

            self.ratio_box

        )



        layout.addWidget(

            QLabel(
                "X Coordinate"
            )

        )

        layout.addWidget(

            self.x_spin

        )



        layout.addWidget(

            QLabel(
                "Y Coordinate"
            )

        )

        layout.addWidget(

            self.y_spin

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



        layout.addStretch()



        self.setLayout(

            layout

        )


        self.update_mode()







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







    def update_mode(
        self
    ):


        mode = self.mode_box.currentText()



        self.width_spin.setEnabled(

            mode in [

                "fixed",

                "coordinates"

            ]

        )


        self.height_spin.setEnabled(

            mode in [

                "fixed",

                "coordinates"

            ]

        )


        self.percent_spin.setEnabled(

            mode == "percentage"

        )


        self.ratio_box.setEnabled(

            mode == "aspect_ratio"

        )


        self.x_spin.setEnabled(

            mode == "coordinates"

        )


        self.y_spin.setEnabled(

            mode == "coordinates"

        )







    def get_output_folder(
        self
    ):


        config = Path(

            "config/app_settings.json"

        )


        if config.exists():


            try:


                with open(

                    config,

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






        mode = self.mode_box.currentText()



        operation = {


            "type":

                "crop",


            "mode":

                mode

        }




        if mode == "fixed":


            operation.update({

                "width":

                    self.width_spin.value(),


                "height":

                    self.height_spin.value()

            })



        elif mode == "percentage":


            operation["value"] = (

                self.percent_spin.value()

            )



        elif mode == "aspect_ratio":


            operation["ratio"] = (

                self.ratio_box.currentText()

            )



        elif mode == "coordinates":


            operation.update({

                "x":

                    self.x_spin.value(),


                "y":

                    self.y_spin.value(),


                "width":

                    self.width_spin.value(),


                "height":

                    self.height_spin.value()

            })








        output_folder = self.get_output_folder()


        output_folder.mkdir(

            parents=True,

            exist_ok=True

        )



        output_path = output_folder / (

            self.selected_file.stem

            +

            "_cropped"

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

                "Crop Error",

                str(error)

            )