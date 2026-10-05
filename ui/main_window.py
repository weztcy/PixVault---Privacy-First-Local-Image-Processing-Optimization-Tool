from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton
)


from PySide6.QtCore import Qt


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

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )



        # =====================
        # HEADER
        # =====================


        header_layout = QHBoxLayout()

        header_layout.setContentsMargins(
            15,
            0,
            15,
            0
        )


        header = QWidget()


        header.setFixedHeight(
            50
        )


        header_layout_inner = QHBoxLayout(
            header
        )


        header_layout_inner.setContentsMargins(
            0,
            0,
            0,
            0
        )



        title = QLabel(
            "PixVault"
        )


        title.setAlignment(
            Qt.AlignmentFlag.AlignVCenter
        )



        local_status = QLabel(
            "🔒 Processing locally"
        )


        local_status.setAlignment(
            Qt.AlignmentFlag.AlignVCenter
        )



        settings_button = QPushButton(
            "⚙ Settings"
        )


        settings_button.clicked.connect(
            lambda:
            self.workspace.show_page(
                "settings"
            )
        )



        header_layout_inner.addWidget(
            title
        )


        header_layout_inner.addStretch()


        header_layout_inner.addWidget(
            local_status
        )


        header_layout_inner.addWidget(
            settings_button
        )



        # =====================
        # CONTENT
        # =====================


        content_layout = QHBoxLayout()


        content_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )


        self.sidebar = Sidebar()



        self.sidebar.setFixedWidth(
            220
        )



        self.workspace = Workspace(

            self.image_service,

            self.batch_service,

            self.history_service

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


            button = self.sidebar.buttons.get(
                button_name
            )


            if button:


                button.clicked.connect(

                    lambda checked=False, name=page_name:

                    self.workspace.show_page(
                        name
                    )

                )