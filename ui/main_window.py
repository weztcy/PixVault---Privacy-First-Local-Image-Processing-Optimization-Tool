from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel
)


from ui.sidebar import Sidebar
from ui.workspace import Workspace


from services.image_service import ImageService
from services.batch_service import BatchService
from services.history_service import HistoryService




class MainWindow(QMainWindow):


    def __init__(
        self
    ):

        super().__init__()


        self.setWindowTitle(
            "PixVault"
        )


        self.resize(
            1280,
            800
        )


        self.setup_services()


        self.setup_ui()



    def setup_services(
        self
    ):


        self.image_service = ImageService()


        self.batch_service = BatchService()


        self.history_service = HistoryService()



    def setup_ui(
        self
    ):


        container = QWidget()


        main_layout = QVBoxLayout()



        header = QLabel(
            "PixVault | Local Processing"
        )


        header.setFixedHeight(
            40
        )



        content_layout = QHBoxLayout()



        self.sidebar = Sidebar()



        self.workspace = Workspace(

            self.image_service,

            self.batch_service,

            self.history_service

        )



        self.sidebar.setFixedWidth(
            220
        )



        content_layout.addWidget(
            self.sidebar
        )


        content_layout.addWidget(
            self.workspace
        )



        main_layout.addWidget(
            header
        )


        main_layout.addLayout(
            content_layout
        )



        container.setLayout(
            main_layout
        )


        self.setCentralWidget(
            container
        )


        self.connect_navigation()



    def connect_navigation(
        self
    ):


        routes = {

            "home":
                "home",

            "all_processing":
                "all_processing",


            "convert":
                "convert",

            "compress":
                "compress",

            "resize":
                "resize",

            "crop":
                "crop",

            "transform":
                "transform",

            "dpi":
                "dpi",

            "metadata":
                "metadata",

            "colorspace":
                "colorspace",

            "bitdepth":
                "bitdepth",


            "history":
                "history",

            "settings":
                "settings",

            "privacy":
                "privacy"

        }



        for button_name, page_name in routes.items():


            self.sidebar.buttons[button_name].clicked.connect(

                lambda checked=False, name=page_name:

                self.workspace.show_page(
                    name
                )

            )