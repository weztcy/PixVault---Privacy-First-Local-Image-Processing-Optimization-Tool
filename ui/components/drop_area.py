from pathlib import Path


from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)


from PySide6.QtCore import (
    Signal,
    Qt
)


from PySide6.QtGui import (
    QDragEnterEvent,
    QDropEvent
)





class DropArea(QWidget):


    files_dropped = Signal(
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


        self.setAcceptDrops(
            True
        )


        self.setup_ui()







    def setup_ui(
        self
    ):


        layout = QVBoxLayout()


        self.label = QLabel(

            "Drag & Drop Images or Folder Here"

        )


        self.label.setAlignment(

            Qt.AlignmentFlag.AlignCenter

        )


        self.label.setMinimumHeight(

            120

        )


        self.label.setObjectName(

            "drop_area"

        )


        layout.addWidget(

            self.label

        )


        self.setLayout(

            layout

        )







    def dragEnterEvent(
        self,
        event: QDragEnterEvent
    ):


        if event.mimeData().hasUrls():


            event.acceptProposedAction()







    def dropEvent(
        self,
        event: QDropEvent
    ):


        urls = event.mimeData().urls()


        files = []



        for url in urls:


            path = Path(

                url.toLocalFile()

            )


            if path.is_file():


                if self.is_supported_image(

                    path

                ):


                    files.append(

                        path

                    )



            elif path.is_dir():


                files.extend(

                    self.scan_folder(

                        path

                    )

                )



        if files:


            self.files_dropped.emit(

                files

            )



        event.acceptProposedAction()







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