from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QMessageBox
)


from PySide6.QtCore import Qt





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


        layout.setSpacing(
            10
        )



        title = QLabel(
            "Processing History"
        )


        title.setObjectName(
            "page_title"
        )



        self.list_widget = QListWidget()


        self.list_widget.setWordWrap(
            True
        )



        refresh_button = QPushButton(
            "Refresh"
        )


        refresh_button.clicked.connect(
            self.load_history
        )



        clear_button = QPushButton(
            "Clear History"
        )


        clear_button.clicked.connect(
            self.clear_history
        )



        layout.addWidget(
            title
        )


        layout.addWidget(
            self.list_widget
        )


        layout.addWidget(
            refresh_button
        )


        layout.addWidget(
            clear_button
        )



        self.setLayout(
            layout
        )








    def load_history(
        self
    ):


        self.list_widget.clear()



        try:


            history = self.history_service.get_history()



        except Exception as error:


            QMessageBox.critical(

                self,

                "History Error",

                str(error)

            )


            return






        if not history:


            self.list_widget.addItem(

                "No processing history"

            )


            return







        for item in history:



            status = item.get(

                "status",

                "unknown"

            )



            source = item.get(

                "source",

                "-"

            )



            output = item.get(

                "output",

                "-"

            )



            format_name = item.get(

                "format",

                "-"

            )



            operations = item.get(

                "operations",

                []

            )



            error = item.get(

                "error"

            )



            text = self.format_history_item(

                status,

                source,

                output,

                format_name,

                operations,

                error

            )



            list_item = QListWidgetItem(

                text

            )


            list_item.setTextAlignment(

                Qt.AlignmentFlag.AlignLeft

            )


            self.list_widget.addItem(

                list_item

            )








    def format_history_item(
        self,
        status,
        source,
        output,
        format_name,
        operations,
        error=None
    ):


        if status == "success":

            icon = "✓"

        else:

            icon = "✕"





        operation_text = ", ".join(

            [

                op.get(

                    "type",

                    "unknown"

                )

                for op in operations

                if isinstance(

                    op,

                    dict

                )

            ]

        )



        if not operation_text:

            operation_text = "-"





        text = (

            f"{icon} {status.upper()}\n\n"

            f"Source:\n"

            f"{source}\n\n"

            f"Output:\n"

            f"{output}\n\n"

            f"Format:\n"

            f"{format_name}\n\n"

            f"Operations:\n"

            f"{operation_text}"

        )





        if error:


            text += (

                "\n\n"

                "Error:\n"

                f"{error}"

            )



        return text








    def clear_history(
        self
    ):


        confirm = QMessageBox.question(

            self,

            "Clear History",

            "Delete all history records?"

        )



        if confirm != QMessageBox.StandardButton.Yes:

            return





        try:


            self.history_service.clear_history()



            self.load_history()



        except Exception as error:


            QMessageBox.critical(

                self,

                "Clear History Error",

                str(error)

            )