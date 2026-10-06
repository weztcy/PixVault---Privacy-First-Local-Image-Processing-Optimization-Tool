from pathlib import Path


from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QProgressBar,
    QPushButton
)


from PySide6.QtCore import Signal


from PySide6.QtGui import QDesktopServices


from PySide6.QtCore import QUrl





class ExportProgress(QWidget):


    open_folder_requested = Signal()





    def __init__(
        self
    ):

        super().__init__()


        self.output_folder = None


        self.setup_ui()







    def setup_ui(
        self
    ):


        layout = QVBoxLayout()



        title = QLabel(
            "Export Progress"
        )



        self.progress_bar = QProgressBar()



        self.progress_bar.setRange(

            0,

            100

        )



        self.status_label = QLabel(
            "Ready"
        )


        self.file_label = QLabel(
            "File: -"
        )



        self.counter_label = QLabel(
            "0 / 0"
        )



        self.open_button = QPushButton(
            "Open Folder"
        )



        self.open_button.clicked.connect(

            self.open_folder

        )



        layout.addWidget(

            title

        )


        layout.addWidget(

            self.progress_bar

        )


        layout.addWidget(

            self.file_label

        )


        layout.addWidget(

            self.counter_label

        )


        layout.addWidget(

            self.status_label

        )


        layout.addWidget(

            self.open_button

        )



        self.setLayout(

            layout

        )








    def set_output_folder(
        self,
        folder
    ):


        self.output_folder = Path(

            folder

        )








    def update_progress(
        self,
        current,
        total,
        filename
    ):


        if total <= 0:

            return



        percentage = int(

            (

                current /

                total

            )

            *

            100

        )



        self.progress_bar.setValue(

            percentage

        )



        self.file_label.setText(

            f"Processing: {filename}"

        )


        self.counter_label.setText(

            f"{current} / {total}"

        )


        self.status_label.setText(

            "Processing"

        )








    def finished(
        self
    ):


        self.progress_bar.setValue(

            100

        )


        self.status_label.setText(

            "Completed"

        )


        self.file_label.setText(

            "Finished"

        )








    def failed(
        self,
        error
    ):


        self.status_label.setText(

            "Failed"

        )


        self.file_label.setText(

            str(error)

        )








    def reset(
        self
    ):


        self.progress_bar.setValue(

            0

        )


        self.status_label.setText(

            "Ready"

        )


        self.file_label.setText(

            "File: -"

        )


        self.counter_label.setText(

            "0 / 0"

        )








    def open_folder(
        self
    ):


        if not self.output_folder:

            return



        if self.output_folder.exists():


            QDesktopServices.openUrl(

                QUrl.fromLocalFile(

                    str(

                        self.output_folder

                    )

                )

            )