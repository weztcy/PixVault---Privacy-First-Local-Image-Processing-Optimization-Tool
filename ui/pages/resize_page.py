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
    QCheckBox,
    QMessageBox
)





class ResizePage(QWidget):



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
                "Resize Image"
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
                "Resize Method"
            )
        )


        self.method_box = QComboBox()


        self.method_box.addItems(

            [

                "exact",

                "width",

                "height",

                "percentage",

                "longest_side",

                "shortest_side"

            ]

        )


        self.method_box.currentTextChanged.connect(

            self.update_method

        )


        layout.addWidget(
            self.method_box
        )





        layout.addWidget(
            QLabel(
                "Width"
            )
        )


        self.width_spin = QSpinBox()


        self.width_spin.setRange(

            1,

            100000

        )


        self.width_spin.setValue(

            1920

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

            100000

        )


        self.height_spin.setValue(

            1080

        )


        layout.addWidget(
            self.height_spin
        )






        layout.addWidget(
            QLabel(
                "Value"
            )
        )


        self.value_spin = QSpinBox()


        self.value_spin.setRange(

            1,

            100000

        )


        self.value_spin.setValue(

            800

        )


        layout.addWidget(
            self.value_spin
        )






        self.keep_ratio = QCheckBox(

            "Keep Aspect Ratio"

        )


        self.keep_ratio.setChecked(

            True

        )


        layout.addWidget(
            self.keep_ratio
        )







        layout.addWidget(
            QLabel(
                "Resampling"
            )
        )


        self.resampling_box = QComboBox()


        self.resampling_box.addItems(

            [

                "lanczos",

                "bicubic",

                "bilinear",

                "nearest"

            ]

        )


        layout.addWidget(
            self.resampling_box
        )





        process = QPushButton(
            "Resize"
        )


        process.clicked.connect(

            self.resize_image

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



        self.update_method()







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








    def update_method(
        self
    ):


        method = self.method_box.currentText()


        exact = method == "exact"


        self.width_spin.setEnabled(

            exact

        )


        self.height_spin.setEnabled(

            exact

        )


        self.value_spin.setEnabled(

            not exact

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








    def resize_image(
        self
    ):


        if not self.selected_file:


            QMessageBox.warning(

                self,

                "Warning",

                "Select image first"

            )


            return






        method = self.method_box.currentText()



        operation = {


            "type":

                "resize",



            "method":

                method,



            "keep_ratio":

                self.keep_ratio.isChecked(),



            "resampling":

                self.resampling_box.currentText()

        }




        if method == "exact":


            operation["width"] = (

                self.width_spin.value()

            )


            operation["height"] = (

                self.height_spin.value()

            )



        else:


            operation["value"] = (

                self.value_spin.value()

            )







        output_folder = self.get_output_folder()


        output_folder.mkdir(

            parents=True,

            exist_ok=True

        )



        output_path = output_folder / (

            self.selected_file.stem

            +

            "_resized"

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

                "Resize Error",

                str(error)

            )