from pathlib import Path


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QHBoxLayout
)


from PySide6.QtCore import Signal





class ImageListWidget(QWidget):


    image_selected = Signal(
        Path
    )


    images_changed = Signal(
        list
    )



    def __init__(
        self
    ):

        super().__init__()


        self.images = []


        self.setup_ui()







    def setup_ui(
        self
    ):


        layout = QVBoxLayout()


        self.list_widget = QListWidget()



        # static height
        self.list_widget.setFixedHeight(
            250
        )



        self.list_widget.itemClicked.connect(
            self.select_item
        )



        button_layout = QHBoxLayout()



        self.remove_button = QPushButton(
            "Remove Selected"
        )


        self.delete_all_button = QPushButton(
            "Delete All"
        )



        self.remove_button.clicked.connect(
            self.remove_selected
        )


        self.delete_all_button.clicked.connect(
            self.delete_all
        )



        button_layout.addWidget(
            self.remove_button
        )


        button_layout.addWidget(
            self.delete_all_button
        )



        layout.addWidget(
            self.list_widget
        )


        layout.addLayout(
            button_layout
        )



        self.setLayout(
            layout
        )







    def set_images(
        self,
        images
    ):


        self.images = [

            Path(image)

            for image in images

        ]


        self.refresh()







    def refresh(
        self
    ):


        self.list_widget.clear()



        for image in self.images:


            self.list_widget.addItem(

                image.name

            )



        self.images_changed.emit(

            self.images.copy()

        )







    def select_item(
        self,
        item
    ):


        index = self.list_widget.row(

            item

        )


        if index >= 0 and index < len(

            self.images

        ):


            self.image_selected.emit(

                self.images[index]

            )








    def remove_selected(
        self
    ):


        row = self.list_widget.currentRow()



        if row < 0:

            return



        del self.images[row]


        self.refresh()







    def delete_all(
        self
    ):


        self.images.clear()


        self.refresh()







    def get_images(
        self
    ):


        return self.images.copy()