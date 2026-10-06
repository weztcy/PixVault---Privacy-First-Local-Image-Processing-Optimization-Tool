from pathlib import Path


from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog
)


from PySide6.QtCore import Signal


from ui.components.drop_area import DropArea





class ImageImporter(QWidget):


    images_added = Signal(
        list
    )



    SUPPORTED_EXTENSIONS = {

        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".avif",
        ".gif",
        ".bmp",
        ".tiff",
        ".tif",
        ".heic",
        ".heif",
        ".ico",
        ".svg"

    }





    def __init__(
        self
    ):

        super().__init__()


        self.images = []


        self.setup_ui()







    def setup_ui(
        self
    ):


        main_layout = QVBoxLayout()



        button_layout = QHBoxLayout()



        self.add_image_button = QPushButton(
            "Add Image"
        )


        self.add_folder_button = QPushButton(
            "Add Folder"
        )



        self.add_image_button.clicked.connect(
            self.add_images
        )


        self.add_folder_button.clicked.connect(
            self.add_folder
        )



        button_layout.addWidget(
            self.add_image_button
        )


        button_layout.addWidget(
            self.add_folder_button
        )



        self.drop_area = DropArea()



        self.drop_area.files_dropped.connect(
            self.add_files
        )



        main_layout.addLayout(
            button_layout
        )


        main_layout.addWidget(
            self.drop_area
        )


        self.setLayout(
            main_layout
        )







    def add_images(
        self
    ):


        files, _ = QFileDialog.getOpenFileNames(

            self,

            "Select Images",

            "",

            (
                "Images "
                "(*.jpg *.jpeg *.png *.webp *.avif "
                "*.gif *.bmp *.tiff *.tif "
                "*.heic *.heif *.ico *.svg)"
            )

        )



        if files:


            self.add_files(

                [

                    Path(file)

                    for file in files

                ]

            )








    def add_folder(
        self
    ):


        folder = QFileDialog.getExistingDirectory(

            self,

            "Select Image Folder"

        )



        if folder:


            files = self.scan_folder(

                Path(folder)

            )


            self.add_files(

                files

            )








    def add_files(
        self,
        files
    ):


        added = []



        for file in files:


            path = Path(

                file

            )



            if not self.is_supported_image(

                path

            ):


                continue



            if path not in self.images:


                self.images.append(

                    path

                )


                added.append(

                    path

                )



        if added:


            self.images_added.emit(

                self.images.copy()

            )








    def scan_folder(
        self,
        folder
    ):


        result = []



        for file in folder.rglob(

            "*"

        ):


            if file.is_file():

                if self.is_supported_image(

                    file

                ):


                    result.append(

                        file

                    )



        return result







    def is_supported_image(
        self,
        path
    ):


        return (

            path.suffix.lower()

            in

            self.SUPPORTED_EXTENSIONS

        )







    def get_images(
        self
    ):


        return self.images.copy()







    def clear(
        self
    ):


        self.images.clear()