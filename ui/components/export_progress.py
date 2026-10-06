from pathlib import Path


from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QProgressBar,
    QPushButton
)


from PySide6.QtCore import (
    Signal,
    QUrl
)


from PySide6.QtGui import (
    QDesktopServices
)






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


        layout = QVBoxLayout(
            self
        )


        layout.setSpacing(
            8
        )



        title = QLabel(
            "Export Progress"
        )


        title.setObjectName(
            "section_title"
        )



        self.progress_bar = QProgressBar()


        self.progress_bar.setRange(
            0,
            100
        )


        self.progress_bar.setValue(
            0
        )



        self.file_label = QLabel(
            "File: -"
        )



        self.counter_label = QLabel(
            "0 / 0"
        )



        self.status_label = QLabel(
            "Ready"
        )



        self.open_button = QPushButton(
            "Open Output Folder"
        )


        self.open_button.clicked.connect(
            self.open_folder
        )


        self.open_button.setEnabled(
            False
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


        if not folder:

            self.output_folder = None

            self.open_button.setEnabled(
                False
            )

            return



        self.output_folder = Path(
            folder
        )


        self.open_button.setEnabled(
            True
        )








    def update_progress(
        self,
        current,
        total,
        filename,
        status
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



        percentage = max(

            0,

            min(

                100,

                percentage

            )

        )



        self.progress_bar.setValue(
            percentage
        )



        self.file_label.setText(

            f"File: {filename}"

        )



        self.counter_label.setText(

            f"{current} / {total}"

        )



        self.status_label.setText(

            status

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
            "All files finished"
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


        self.file_label.setText(
            "File: -"
        )


        self.counter_label.setText(
            "0 / 0"
        )


        self.status_label.setText(
            "Ready"
        )








    def open_folder(
        self
    ):


        if not self.output_folder:

            return



        if not self.output_folder.exists():

            return



        QDesktopServices.openUrl(

            QUrl.fromLocalFile(

                str(
                    self.output_folder
                )

            )

        )