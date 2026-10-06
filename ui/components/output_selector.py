from pathlib import Path


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


        self.default_folder = Path(

            default_folder

        ) if default_folder else Path(
            "output"
        )


        self.custom_folder = None


        self.setup_ui()


        self.update_output()







    def setup_ui(
        self
    ):


        layout = QVBoxLayout()



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



        self.radio_group = QButtonGroup()


        self.radio_group.addButton(

            self.default_radio

        )


        self.radio_group.addButton(

            self.custom_radio

        )



        self.default_radio.toggled.connect(
            self.update_output
        )


        self.custom_radio.toggled.connect(
            self.update_output
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



        browse_layout = QHBoxLayout()



        browse_layout.addWidget(

            self.folder_input

        )


        browse_layout.addWidget(

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

            browse_layout

        )



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


        if self.custom_radio.isChecked():


            if self.custom_folder:


                folder = self.custom_folder


            else:


                folder = self.default_folder



        else:


            folder = self.default_folder



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








    def set_default_folder(
        self,
        folder
    ):


        self.default_folder = Path(

            folder

        )


        self.update_output()