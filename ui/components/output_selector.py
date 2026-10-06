from pathlib import Path
import json


from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QRadioButton,
    QFileDialog,
    QButtonGroup
)


from PySide6.QtCore import Signal






class OutputSelector(QWidget):


    output_changed = Signal(
        Path
    )





    def __init__(
        self,
        default_folder=None
    ):

        super().__init__()



        self.custom_folder = None



        self.default_folder = self.resolve_default_folder(

            default_folder

        )



        self.setup_ui()



        self.update_output()










    def resolve_default_folder(
        self,
        folder
    ):


        if folder:


            return Path(
                folder
            )



        settings_file = Path(
            "config/app_settings.json"
        )



        if settings_file.exists():


            try:


                with open(

                    settings_file,

                    "r",

                    encoding="utf-8"

                ) as file:


                    data = json.load(
                        file
                    )


                    output_folder = data.get(
                        "output_folder"
                    )



                    if output_folder:


                        return Path(
                            output_folder
                        )


            except Exception:


                pass



        return Path(
            "output"
        )









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
            "Output Folder"
        )



        self.default_radio = QRadioButton(
            "Default Folder"
        )


        self.custom_radio = QRadioButton(
            "Custom Folder"
        )



        self.default_radio.setChecked(
            True
        )



        self.radio_group = QButtonGroup(
            self
        )


        self.radio_group.addButton(
            self.default_radio
        )


        self.radio_group.addButton(
            self.custom_radio
        )



        self.folder_input = QLineEdit()


        self.folder_input.setReadOnly(
            True
        )



        browse_button = QPushButton(
            "Browse"
        )


        browse_button.clicked.connect(
            self.select_folder
        )



        folder_layout = QHBoxLayout()


        folder_layout.addWidget(
            self.folder_input
        )


        folder_layout.addWidget(
            browse_button
        )



        layout.addWidget(
            title
        )


        layout.addWidget(
            self.default_radio
        )


        layout.addWidget(
            self.custom_radio
        )


        layout.addLayout(
            folder_layout
        )



        self.setLayout(
            layout
        )



        self.default_radio.toggled.connect(
            self.update_output
        )


        self.custom_radio.toggled.connect(
            self.update_output
        )









    def select_folder(
        self
    ):


        folder = QFileDialog.getExistingDirectory(

            self,

            "Select Output Folder"

        )



        if not folder:


            return



        self.custom_folder = Path(
            folder
        )



        self.custom_radio.setChecked(
            True
        )



        self.update_output()










    def update_output(
        self
    ):


        folder = self.get_output_folder()



        self.folder_input.setText(
            str(folder)
        )



        self.output_changed.emit(
            folder
        )










    def get_output_folder(
        self
    ):


        if self.custom_radio.isChecked():


            if self.custom_folder:


                return self.custom_folder



        return self.default_folder










    def get_current_folder(
        self
    ):


        return self.get_output_folder()










    def set_default_folder(
        self,
        folder
    ):


        self.default_folder = Path(
            folder
        )


        if self.default_radio.isChecked():

            self.update_output()