from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QFrame,
    QComboBox,
    QSpinBox,
    QMessageBox
)


from ui.components.image_importer import ImageImporter
from ui.components.image_list_widget import ImageListWidget
from ui.components.image_preview import ImagePreview
from ui.components.image_info_panel import ImageInfoPanel
from ui.components.output_selector import OutputSelector
from ui.components.export_progress import ExportProgress





class CropPage(QWidget):


    def __init__(
        self,
        image_service,
        batch_service
    ):

        super().__init__()


        self.image_service = image_service

        self.batch_service = batch_service


        self.images = []

        self.output_folder = None


        self.setup_ui()

        self.connect_events()








    def setup_ui(
        self
    ):


        root_layout = QVBoxLayout(
            self
        )


        self.scroll_area = QScrollArea()


        self.scroll_area.setWidgetResizable(
            True
        )


        container = QWidget()


        self.layout = QVBoxLayout(
            container
        )


        self.layout.setSpacing(
            15
        )



        title = QLabel(
            "Crop Image"
        )


        title.setObjectName(
            "page_title"
        )



        self.importer = ImageImporter()


        self.image_list = ImageListWidget()



        preview_layout = QHBoxLayout()



        self.preview = ImagePreview()


        self.info_panel = ImageInfoPanel()



        preview_layout.addWidget(
            self.preview
        )


        preview_layout.addWidget(
            self.info_panel
        )



        crop_box = QFrame()


        crop_layout = QVBoxLayout(
            crop_box
        )


        crop_layout.addWidget(
            QLabel(
                "Crop Settings"
            )
        )



        crop_layout.addWidget(
            QLabel(
                "Crop Mode"
            )
        )



        self.mode_box = QComboBox()


        self.mode_box.addItems(
            [
                "fixed",
                "percentage",
                "aspect_ratio",
                "coordinates"
            ]
        )


        crop_layout.addWidget(
            self.mode_box
        )



        crop_layout.addWidget(
            QLabel(
                "Width"
            )
        )


        self.width_spin = QSpinBox()


        self.width_spin.setRange(
            1,
            100000
        )


        self.width_spin.setValue(
            500
        )


        crop_layout.addWidget(
            self.width_spin
        )



        crop_layout.addWidget(
            QLabel(
                "Height"
            )
        )


        self.height_spin = QSpinBox()


        self.height_spin.setRange(
            1,
            100000
        )


        self.height_spin.setValue(
            500
        )


        crop_layout.addWidget(
            self.height_spin
        )



        crop_layout.addWidget(
            QLabel(
                "Percentage"
            )
        )


        self.percent_spin = QSpinBox()


        self.percent_spin.setRange(
            1,
            100
        )


        self.percent_spin.setValue(
            50
        )


        crop_layout.addWidget(
            self.percent_spin
        )



        crop_layout.addWidget(
            QLabel(
                "Aspect Ratio"
            )
        )


        self.ratio_box = QComboBox()


        self.ratio_box.addItems(
            [
                "1:1",
                "4:3",
                "16:9",
                "3:2",
                "9:16"
            ]
        )


        crop_layout.addWidget(
            self.ratio_box
        )



        crop_layout.addWidget(
            QLabel(
                "X Coordinate"
            )
        )


        self.x_spin = QSpinBox()


        self.x_spin.setRange(
            0,
            100000
        )


        crop_layout.addWidget(
            self.x_spin
        )



        crop_layout.addWidget(
            QLabel(
                "Y Coordinate"
            )
        )


        self.y_spin = QSpinBox()


        self.y_spin.setRange(
            0,
            100000
        )


        crop_layout.addWidget(
            self.y_spin
        )



        self.output_selector = OutputSelector()


        self.progress = ExportProgress()



        self.start_button = QPushButton(
            "Start Crop"
        )



        self.layout.addWidget(
            title
        )


        self.layout.addWidget(
            self.importer
        )


        self.layout.addWidget(
            self.image_list
        )


        self.layout.addLayout(
            preview_layout
        )


        self.layout.addWidget(
            crop_box
        )


        self.layout.addWidget(
            self.output_selector
        )


        self.layout.addWidget(
            self.progress
        )


        self.layout.addWidget(
            self.start_button
        )


        self.layout.addStretch()



        self.scroll_area.setWidget(
            container
        )


        root_layout.addWidget(
            self.scroll_area
        )








    def connect_events(
        self
    ):


        self.importer.images_added.connect(
            self.load_images
        )


        self.image_list.image_selected.connect(
            self.show_preview
        )


        self.output_selector.output_changed.connect(
            self.set_output_folder
        )


        self.start_button.clicked.connect(
            self.start_crop
        )



        self.mode_box.currentTextChanged.connect(
            self.update_mode
        )


        self.batch_service.progress_changed.connect(
            self.progress.update_progress
        )


        self.batch_service.processing_finished.connect(
            self.crop_finished
        )


        self.batch_service.processing_error.connect(
            self.crop_error
        )



        self.update_mode()








    def load_images(
        self,
        images
    ):


        self.images = images


        self.image_list.set_images(
            images
        )


        if images:

            self.show_preview(
                images[0]
            )








    def show_preview(
        self,
        image
    ):


        self.preview.set_image(
            image
        )


        self.info_panel.set_image(
            image
        )








    def set_output_folder(
        self,
        folder
    ):


        self.output_folder = folder








    def update_mode(
        self
    ):


        mode = self.mode_box.currentText()


        self.width_spin.setEnabled(
            mode in [
                "fixed",
                "coordinates"
            ]
        )


        self.height_spin.setEnabled(
            mode in [
                "fixed",
                "coordinates"
            ]
        )


        self.percent_spin.setEnabled(
            mode == "percentage"
        )


        self.ratio_box.setEnabled(
            mode == "aspect_ratio"
        )


        self.x_spin.setEnabled(
            mode == "coordinates"
        )


        self.y_spin.setEnabled(
            mode == "coordinates"
        )








    def build_config(
        self
    ):


        mode = self.mode_box.currentText()


        operation = {

            "type":
                "crop",

            "mode":
                mode

        }



        if mode == "fixed":


            operation.update({

                "width":
                    self.width_spin.value(),

                "height":
                    self.height_spin.value()

            })



        elif mode == "percentage":


            operation["value"] = (

                self.percent_spin.value()

            )



        elif mode == "aspect_ratio":


            operation["ratio"] = (

                self.ratio_box.currentText()

            )



        elif mode == "coordinates":


            operation.update({

                "x":
                    self.x_spin.value(),

                "y":
                    self.y_spin.value(),

                "width":
                    self.width_spin.value(),

                "height":
                    self.height_spin.value()

            })



        return {

            "operations":
                [
                    operation
                ],


            "output":
                {
                    "keep_format": True
                }

        }








    def start_crop(
        self
    ):


        if not self.images:


            QMessageBox.warning(
                self,
                "Crop",
                "No images selected"
            )


            return



        if not self.output_folder:


            QMessageBox.warning(
                self,
                "Crop",
                "Output folder not selected"
            )


            return



        self.start_button.setEnabled(
            False
        )



        self.progress.reset()



        try:


            self.batch_service.start_batch(

                self.images,

                self.output_folder,

                self.build_config()

            )


            self.progress.set_output_folder(

                self.output_folder

            )



        except Exception as error:


            self.start_button.setEnabled(
                True
            )


            QMessageBox.critical(

                self,

                "Crop Error",

                str(error)

            )








    def crop_finished(
        self,
        result
    ):


        self.start_button.setEnabled(
            True
        )


        self.progress.finished()








    def crop_error(
        self,
        error
    ):


        self.start_button.setEnabled(
            True
        )


        self.progress.failed(
            error
        )