from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QListWidget,
    QPushButton
)




class HistoryPage(QWidget):


    def __init__(
        self,
        history_service
    ):

        super().__init__()


        self.history_service = history_service


        self.setup_ui()


        self.load_history()



    def setup_ui(
        self
    ):


        layout = QVBoxLayout()



        title = QLabel(
            "History"
        )


        self.list_widget = QListWidget()



        self.refresh_button = QPushButton(
            "Refresh"
        )


        self.refresh_button.clicked.connect(
            self.load_history
        )



        layout.addWidget(
            title
        )


        layout.addWidget(
            self.list_widget
        )


        layout.addWidget(
            self.refresh_button
        )



        self.setLayout(
            layout
        )



    def load_history(
        self
    ):


        self.list_widget.clear()


        history = self.history_service.get_history()



        for item in history:


            text = (

                f"Source: {item['source']}\n"

                f"Output: {item['output']}\n"

                f"Format: {item['format']}\n"

                f"Status: {item['status']}"

            )


            self.list_widget.addItem(
                text
            )