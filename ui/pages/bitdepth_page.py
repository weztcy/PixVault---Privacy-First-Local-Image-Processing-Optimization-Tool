from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


from ui.components.export_progress import ExportProgress
from ui.components.image_importer import ImageImporter

from ui.components.processing_options.common.format_support_info import (
    FormatSupportInfo
)

from ui.components.image_info_panel import ImageInfoPanel
from ui.components.image_list_widget import ImageListWidget
from ui.components.image_preview import ImagePreview
from ui.components.output_selector import OutputSelector
from ui.components.processing_options.bitdepth_options import BitDepthOptions





class BitDepthPage(QWidget):


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
            "Bit Depth Processor"
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







        # =====================
        # BIT DEPTH OPTIONS
        # =====================


        settings_box = QFrame()


        settings_layout = QVBoxLayout(
            settings_box
        )


        settings_layout.addWidget(
            QLabel(
                "Bit Depth Settings"
            )
        )


        self.bitdepth_options = BitDepthOptions()


        settings_layout.addWidget(
            self.bitdepth_options
        )








        # =====================
        # FORMAT SUPPORT
        # =====================


        self.format_support = FormatSupportInfo(
            "bitdepth"
        )








        self.output_selector = OutputSelector()


        self.output_folder = (
            self.output_selector.get_output_folder()
        )



        self.start_button = QPushButton(
            "Apply Bit Depth"
        )


        self.progress = ExportProgress()



        self.cancel_button = QPushButton(
            "Cancel Processing"
        )


        self.cancel_button.hide()







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
            settings_box
        )


        self.layout.addWidget(
            self.format_support
        )


        self.layout.addWidget(
            self.output_selector
        )


        self.layout.addWidget(
            self.start_button
        )


        self.layout.addWidget(
            self.progress
        )


        self.layout.addWidget(
            self.cancel_button
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
            self.start_bitdepth
        )


        self.cancel_button.clicked.connect(
            self.cancel_processing
        )


        self.batch_service.progress_changed.connect(
            self.progress.update_progress
        )


        self.batch_service.processing_finished.connect(
            self.bitdepth_finished
        )


        self.batch_service.processing_error.connect(
            self.bitdepth_error
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


        operation = self.bitdepth_options.get_settings()


        operation["type"] = "bitdepth"



        return {

            "operations": [
                operation
            ],

            "output": {
                "keep_format": True
            }

        }








    def start_bitdepth(
        self
    ):


        if not self.images:

            QMessageBox.warning(
                self,
                "Bit Depth",
                "No images selected"
            )

            return



        if not self.output_folder:

            QMessageBox.warning(
                self,
                "Bit Depth",
                "Output folder not selected"
            )

            return






        self.start_button.setEnabled(
            False
        )


        self.cancel_button.show()


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


            self.cancel_button.hide()


            QMessageBox.critical(

                self,

                "Bit Depth Error",

                str(error)

            )









    def cancel_processing(
        self
    ):


        try:

            self.batch_service.cancel()

        except Exception:

            pass



        self.start_button.setEnabled(
            True
        )


        self.cancel_button.hide()







    def bitdepth_finished(
        self,
        result
    ):


        self.start_button.setEnabled(
            True
        )


        self.cancel_button.hide()


        self.progress.finished()







    def bitdepth_error(
        self,
        error
    ):


        self.start_button.setEnabled(
            True
        )


        self.cancel_button.hide()


        self.progress.failed(
            error
        )