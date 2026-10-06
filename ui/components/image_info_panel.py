from pathlib import Path


from PIL import Image


from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGroupBox
)





class ImageInfoPanel(QWidget):



    def __init__(
        self
    ):

        super().__init__()


        self.current_image = None


        self.setup_ui()







    def setup_ui(
        self
    ):


        layout = QVBoxLayout()



        title = QLabel(
            "Image Details"
        )



        self.info_box = QGroupBox()



        info_layout = QVBoxLayout()



        self.name_label = QLabel(
            "Name: -"
        )


        self.path_label = QLabel(
            "Path: -"
        )


        self.format_label = QLabel(
            "Format: -"
        )


        self.size_label = QLabel(
            "Size: -"
        )


        self.resolution_label = QLabel(
            "Resolution: -"
        )


        self.mode_label = QLabel(
            "Color Mode: -"
        )


        self.depth_label = QLabel(
            "Bit Depth: -"
        )



        labels = [

            self.name_label,

            self.path_label,

            self.format_label,

            self.size_label,

            self.resolution_label,

            self.mode_label,

            self.depth_label

        ]



        for label in labels:


            label.setWordWrap(

                True

            )


            info_layout.addWidget(

                label

            )



        self.info_box.setLayout(

            info_layout

        )



        layout.addWidget(

            title

        )


        layout.addWidget(

            self.info_box

        )


        layout.addStretch()



        self.setLayout(

            layout

        )








    def set_image(
        self,
        image_path
    ):


        self.current_image = Path(

            image_path

        )



        self.load_information()







    def load_information(
        self
    ):


        if not self.current_image:

            return



        file = self.current_image



        self.name_label.setText(

            f"Name: {file.name}"

        )


        self.path_label.setText(

            f"Path: {file}"

        )



        file_size = self.format_size(

            file.stat().st_size

        )


        self.size_label.setText(

            f"Size: {file_size}"

        )



        try:


            with Image.open(

                file

            ) as image:


                self.format_label.setText(

                    f"Format: {image.format}"

                )


                self.resolution_label.setText(

                    f"Resolution: {image.width} x {image.height}"

                )


                self.mode_label.setText(

                    f"Color Mode: {image.mode}"

                )


                self.depth_label.setText(

                    f"Bit Depth: {self.get_bit_depth(image)}"

                )



        except Exception as error:


            self.format_label.setText(

                f"Format: Unknown ({error})"

            )








    def get_bit_depth(
        self,
        image
    ):


        mode_depth = {


            "1":
                1,


            "L":
                8,


            "P":
                8,


            "RGB":
                8,


            "RGBA":
                8,


            "I;16":
                16

        }



        return (

            f"{mode_depth.get(image.mode, 'Unknown')} bit"

        )








    def format_size(
        self,
        size
    ):


        units = [

            "B",

            "KB",

            "MB",

            "GB"

        ]


        value = float(

            size

        )



        for unit in units:


            if value < 1024:


                return f"{value:.2f} {unit}"



            value /= 1024



        return f"{value:.2f} TB"








    def clear(
        self
    ):


        self.current_image = None



        self.name_label.setText(
            "Name: -"
        )


        self.path_label.setText(
            "Path: -"
        )


        self.format_label.setText(
            "Format: -"
        )


        self.size_label.setText(
            "Size: -"
        )


        self.resolution_label.setText(
            "Resolution: -"
        )


        self.mode_label.setText(
            "Color Mode: -"
        )


        self.depth_label.setText(
            "Bit Depth: -"
        )