from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel
)

from ui.sidebar import Sidebar
from ui.workspace import Workspace


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("PixVault")

        self.resize(
            1280,
            800
        )

        self.setup_ui()


    def setup_ui(self):

        container = QWidget()


        main_layout = QVBoxLayout()


        header = QLabel(
            "PixVault | Local Processing"
        )

        header.setFixedHeight(40)


        content_layout = QHBoxLayout()


        self.sidebar = Sidebar()

        self.workspace = Workspace()


        self.sidebar.setFixedWidth(220)


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



    def connect_navigation(self):

        self.sidebar.buttons["home"].clicked.connect(
            lambda:
            self.workspace.show_page("home")
        )


        self.sidebar.buttons["all_processing"].clicked.connect(
            lambda:
            self.workspace.show_page("all_processing")
        )


        self.sidebar.buttons["history"].clicked.connect(
            lambda:
            self.workspace.show_page("history")
        )


        self.sidebar.buttons["settings"].clicked.connect(
            lambda:
            self.workspace.show_page("settings")
        )


        self.sidebar.buttons["privacy"].clicked.connect(
            lambda:
            self.workspace.show_page("privacy")
        )