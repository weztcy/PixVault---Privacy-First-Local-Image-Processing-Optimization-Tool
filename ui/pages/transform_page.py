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





class TransformPage(QWidget):



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
                "Transform Image"
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


        self.operation_box.currentTextChanged.connect(

            self.update_operation

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


        layout.addStretch()



        self.setLayout(
            layout
        )


        self.update_operation()







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







    def update_operation(
        self
    ):


        operation = self.operation_box.currentText()


        self.angle_spin.setEnabled(

            operation == "rotate"

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


                        return Path(folder)



            except Exception:

                pass



        return Path(
            "output"
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






        operation_name = self.operation_box.currentText()



        operation = {


            "type":

                "transform"

        }




        if operation_name == "rotate":


            operation["rotation"] = (

                self.angle_spin.value()

            )



        elif operation_name == "flip_horizontal":


            operation["flip"] = (

                "horizontal"

            )



        elif operation_name == "flip_vertical":


            operation["flip"] = (

                "vertical"

            )



        elif operation_name == "flip_both":


            operation["flip"] = (

                "both"

            )







        output_folder = self.get_output_folder()


        output_folder.mkdir(

            parents=True,

            exist_ok=True

        )



        output_path = output_folder / (

            self.selected_file.stem

            +

            "_transformed"

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

                "Transform Error",

                str(error)

            )