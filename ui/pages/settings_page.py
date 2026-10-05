from pathlib import Path


from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QFileDialog,
    QMessageBox
)




class SettingsPage(QWidget):


    def __init__(
        self
    ):

        super().__init__()


        self.setup_ui()



    def setup_ui(
        self
    ):


        layout = QVBoxLayout()



        layout.addWidget(
            QLabel(
                "Settings"
            )
        )



        # Default format


        layout.addWidget(
            QLabel(
                "Default Output Format"
            )
        )


        self.format_box = QComboBox()


        self.format_box.addItems(
            [
                "WEBP",
                "JPEG",
                "PNG",
                "AVIF"
            ]
        )


        layout.addWidget(
            self.format_box
        )



        # Quality


        layout.addWidget(
            QLabel(
                "Default Quality"
            )
        )


        self.quality_spin = QSpinBox()


        self.quality_spin.setRange(
            1,
            100
        )


        self.quality_spin.setValue(
            85
        )


        layout.addWidget(
            self.quality_spin
        )



        # Output folder


        layout.addWidget(
            QLabel(
                "Default Output Folder"
            )
        )


        self.output_folder = QLineEdit()


        browse = QPushButton(
            "Select Folder"
        )


        browse.clicked.connect(
            self.select_folder
        )


        layout.addWidget(
            self.output_folder
        )


        layout.addWidget(
            browse
        )



        save = QPushButton(
            "Save Settings"
        )


        save.clicked.connect(
            self.save_settings
        )


        layout.addWidget(
            save
        )



        self.status_label = QLabel()


        layout.addWidget(
            self.status_label
        )


        layout.addStretch()



        self.setLayout(
            layout
        )



    def select_folder(
        self
    ):


        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder"
        )


        if folder:

            self.output_folder.setText(
                folder
            )



    def save_settings(
        self
    ):


        settings = {

            "format":
                self.format_box.currentText(),

            "quality":
                self.quality_spin.value(),

            "output_folder":
                self.output_folder.text()

        }


        self.status_label.setText(
            "Settings saved"
        )


        print(
            settings
        )