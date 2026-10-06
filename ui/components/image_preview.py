from pathlib import Path


from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame
)


from PySide6.QtCore import (
    Qt
)


from PySide6.QtGui import (
    QPixmap
)





class ImagePreview(QWidget):



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
            "Preview"
        )



        self.preview_label = QLabel()



        self.preview_label.setFixedSize(

            400,

            300

        )



        self.preview_label.setAlignment(

            Qt.AlignmentFlag.AlignCenter

        )


        self.preview_label.setFrameShape(

            QFrame.Shape.StyledPanel

        )


        self.preview_label.setText(

            "No Image Selected"

        )



        layout.addWidget(

            title

        )


        layout.addWidget(

            self.preview_label

        )



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



        pixmap = QPixmap(

            str(

                self.current_image

            )

        )



        if pixmap.isNull():


            self.preview_label.setText(

                "Preview unavailable"

            )


            return





        scaled = pixmap.scaled(

            self.preview_label.size(),

            Qt.AspectRatioMode.KeepAspectRatio,

            Qt.TransformationMode.SmoothTransformation

        )



        self.preview_label.setPixmap(

            scaled

        )







    def clear(
        self
    ):


        self.current_image = None


        self.preview_label.clear()


        self.preview_label.setText(

            "No Image Selected"

        )