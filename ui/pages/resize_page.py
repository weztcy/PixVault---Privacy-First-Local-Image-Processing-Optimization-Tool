from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QFrame,
    QSpinBox,
    QComboBox,
    QCheckBox,
    QMessageBox
)


from ui.components.image_importer import ImageImporter
from ui.components.image_list_widget import ImageListWidget
from ui.components.image_preview import ImagePreview
from ui.components.image_info_panel import ImageInfoPanel
from ui.components.output_selector import OutputSelector
from ui.components.export_progress import ExportProgress





class ResizePage(QWidget):


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
            "Resize Image"
        )


        title.setObjectName(
            "page_title"
        )



        self.importer = ImageImporter()



        self.image_list = ImageListWidget()



        preview_container = QHBoxLayout()



        self.preview = ImagePreview()


        self.info_panel = ImageInfoPanel()



        preview_container.addWidget(
            self.preview
        )


        preview_container.addWidget(
            self.info_panel
        )



        settings_box = QFrame()


        settings_layout = QVBoxLayout(
            settings_box
        )



        settings_layout.addWidget(
            QLabel(
                "Resize Settings"
            )
        )



        settings_layout.addWidget(
            QLabel(
                "Method"
            )
        )



        self.method_box = QComboBox()


        self.method_box.addItems(
            [
                "exact",
                "width",
                "height",
                "percentage",
                "longest_side",
                "shortest_side"
            ]
        )


        settings_layout.addWidget(
            self.method_box
        )



        settings_layout.addWidget(
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
            1920
        )


        settings_layout.addWidget(
            self.width_spin
        )



        settings_layout.addWidget(
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
            1080
        )


        settings_layout.addWidget(
            self.height_spin
        )



        settings_layout.addWidget(
            QLabel(
                "Value"
            )
        )



        self.value_spin = QSpinBox()


        self.value_spin.setRange(
            1,
            100000
        )


        self.value_spin.setValue(
            800
        )


        settings_layout.addWidget(
            self.value_spin
        )



        self.keep_ratio = QCheckBox(
            "Keep Aspect Ratio"
        )


        self.keep_ratio.setChecked(
            True
        )


        settings_layout.addWidget(
            self.keep_ratio
        )



        settings_layout.addWidget(
            QLabel(
                "Resampling"
            )
        )



        self.resampling_box = QComboBox()


        self.resampling_box.addItems(
            [
                "lanczos",
                "bicubic",
                "bilinear",
                "nearest"
            ]
        )


        settings_layout.addWidget(
            self.resampling_box
        )



        self.output_selector = OutputSelector()



        self.progress = ExportProgress()



        self.start_button = QPushButton(
            "Start Resize"
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
            preview_container
        )


        self.layout.addWidget(
            settings_box
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
            self.start_resize
        )


        self.batch_service.progress_changed.connect(
            self.progress.update_progress
        )


        self.batch_service.processing_finished.connect(
            self.resize_finished
        )


        self.batch_service.processing_error.connect(
            self.resize_error
        )








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








    def build_config(
        self
    ):


        operation = {

            "type":
                "resize",

            "method":
                self.method_box.currentText(),

            "keep_ratio":
                self.keep_ratio.isChecked(),

            "resampling":
                self.resampling_box.currentText()

        }



        method = self.method_box.currentText()



        if method == "exact":


            operation["width"] = self.width_spin.value()

            operation["height"] = self.height_spin.value()



        else:


            operation["value"] = self.value_spin.value()



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








    def start_resize(
        self
    ):


        if not self.images:


            QMessageBox.warning(
                self,
                "Resize",
                "No images selected"
            )


            return



        if not self.output_folder:


            QMessageBox.warning(
                self,
                "Resize",
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

                "Resize Error",

                str(error)

            )








    def resize_finished(
        self,
        result
    ):


        self.start_button.setEnabled(
            True
        )


        self.progress.finished()








    def resize_error(
        self,
        error
    ):


        self.start_button.setEnabled(
            True
        )


        self.progress.failed(
            error
        )