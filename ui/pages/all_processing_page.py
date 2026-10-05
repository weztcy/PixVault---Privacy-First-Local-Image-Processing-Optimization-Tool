from pathlib import Path


from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QListWidget,
    QCheckBox,
    QGroupBox,
    QMessageBox,
    QLineEdit
)


from ui.components.processing_panel import ProcessingPanel
from ui.components.encoder_options_panel import EncoderOptionsPanel




class AllProcessingPage(QWidget):


    def __init__(
        self,
        image_service,
        batch_service
    ):

        super().__init__()


        self.image_service = image_service

        self.batch_service = batch_service


        self.selected_files = []


        self.setup_ui()



    def setup_ui(
        self
    ):


        layout = QVBoxLayout()



        layout.addWidget(
            QLabel(
                "ALL PROCESSING"
            )
        )



        # =====================
        # INPUT
        # =====================


        input_box = QGroupBox(
            "INPUT"
        )


        input_layout = QVBoxLayout()


        button_layout = QHBoxLayout()



        add_images = QPushButton(
            "Add Images"
        )


        add_images.clicked.connect(
            self.add_images
        )



        add_folder = QPushButton(
            "Add Folder"
        )


        add_folder.clicked.connect(
            self.add_folder
        )



        button_layout.addWidget(
            add_images
        )


        button_layout.addWidget(
            add_folder
        )


        self.subfolder_check = QCheckBox(
            "Include Subfolders"
        )


        input_layout.addLayout(
            button_layout
        )


        input_layout.addWidget(
            self.subfolder_check
        )


        input_box.setLayout(
            input_layout
        )


        layout.addWidget(
            input_box
        )



        # =====================
        # FILE LIST
        # =====================


        image_box = QGroupBox(
            "SELECTED IMAGES"
        )


        image_layout = QVBoxLayout()



        self.file_list = QListWidget()


        image_layout.addWidget(
            self.file_list
        )



        clear_button = QPushButton(
            "Clear All"
        )


        clear_button.clicked.connect(
            self.clear_files
        )


        image_layout.addWidget(
            clear_button
        )



        image_box.setLayout(
            image_layout
        )


        layout.addWidget(
            image_box
        )



        # =====================
        # PROCESSING
        # =====================


        processing_box = QGroupBox(
            "IMAGE PROCESSING"
        )


        processing_layout = QVBoxLayout()



        self.processing_panel = ProcessingPanel()


        processing_layout.addWidget(
            self.processing_panel
        )


        processing_box.setLayout(
            processing_layout
        )


        layout.addWidget(
            processing_box
        )



        # =====================
        # OUTPUT
        # =====================


        output_box = QGroupBox(
            "OUTPUT"
        )


        output_layout = QVBoxLayout()



        self.encoder_panel = EncoderOptionsPanel()


        output_layout.addWidget(
            self.encoder_panel
        )



        output_layout.addWidget(
            QLabel(
                "Output Location"
            )
        )



        self.output_path = QLineEdit()


        self.output_path.setText(
            "test_data/output/all_processing"
        )


        output_layout.addWidget(
            self.output_path
        )



        output_box.setLayout(
            output_layout
        )


        layout.addWidget(
            output_box
        )



        # =====================
        # ACTION
        # =====================


        self.process_button = QPushButton(
            "CONVERT IMAGES"
        )


        self.process_button.clicked.connect(
            self.process
        )


        layout.addWidget(
            self.process_button
        )



        self.result_label = QLabel()


        layout.addWidget(
            self.result_label
        )



        self.setLayout(
            layout
        )



    # =====================
    # FILE INPUT
    # =====================


    def add_images(
        self
    ):


        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images"
        )


        for file in files:

            self.add_file(
                Path(file)
            )



    def add_folder(
        self
    ):


        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder"
        )


        if not folder:

            return



        folder = Path(
            folder
        )


        pattern = (

            "**/*"

            if self.subfolder_check.isChecked()

            else "*"

        )



        extensions = [

            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
            ".bmp",
            ".tiff",
            ".tif",
            ".avif"

        ]



        for file in folder.glob(
            pattern
        ):


            if file.suffix.lower() in extensions:

                self.add_file(
                    file
                )



    def add_file(
        self,
        file
    ):


        if file not in self.selected_files:


            self.selected_files.append(
                file
            )


            self.file_list.addItem(
                str(file)
            )



    def clear_files(
        self
    ):


        self.selected_files.clear()


        self.file_list.clear()



    # =====================
    # PROCESS
    # =====================


    def process(
        self
    ):


        if not self.selected_files:


            QMessageBox.warning(
                self,
                "Warning",
                "No images selected"
            )


            return



        operations = self.processing_panel.get_operations()



        output_config = self.encoder_panel.get_config()



        config = {


            "operations": operations,


            "output": output_config

        }



        self.process_button.setEnabled(
            False
        )



        self.result_label.setText(
            "Starting processing..."
        )



        self.batch_service.start_batch(

            self.selected_files,

            self.output_path.text(),

            config,

            progress_callback=self.update_progress,

            finished_callback=self.processing_finished,

            error_callback=self.processing_error

        )



    # =====================
    # CALLBACKS
    # =====================


    def update_progress(
        self,
        current,
        total,
        filename
    ):


        self.result_label.setText(

            f"Processing {current}/{total}\n{filename}"

        )



    def processing_finished(
        self,
        result
    ):


        self.process_button.setEnabled(
            True
        )


        self.result_label.setText(

            f"Completed:\n{result}"

        )



    def processing_error(
        self,
        error
    ):


        self.process_button.setEnabled(
            True
        )


        QMessageBox.critical(

            self,

            "Processing Error",

            str(error)

        )