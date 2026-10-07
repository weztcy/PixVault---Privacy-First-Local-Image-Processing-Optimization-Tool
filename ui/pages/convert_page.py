from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
)


from ui.components.export_progress import ExportProgress
from ui.components.format_options.format_options_panel import FormatOptionsPanel
from ui.components.image_importer import ImageImporter
from ui.components.drop_area import DropArea

from ui.components.processing_options.common.format_support_info import (
    FormatSupportInfo
)

from ui.components.image_info_panel import ImageInfoPanel
from ui.components.image_list_widget import ImageListWidget
from ui.components.image_preview import ImagePreview
from ui.components.output_selector import OutputSelector





class ConvertPage(QWidget):


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

        self.format_settings = {}



        self.setup_ui()

        self.connect_events()


        self.format_options.set_format(
            self.format_box.currentText()
        )





    def setup_ui(self):


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



        # =====================
        # TITLE
        # =====================


        title = QLabel(
            "Convert Image"
        )


        title.setObjectName(
            "page_title"
        )



        # =====================
        # FORMAT SUPPORT
        # =====================


        self.format_support = FormatSupportInfo(
            "convert"
        )



        # =====================
        # IMAGE IMPORT AREA
        # DROP AREA | IMPORTER
        # =====================


        self.drop_area = DropArea()


        self.importer = ImageImporter()



        self.drop_area.files_dropped.connect(
            self.importer.add_files
        )



        import_layout = QHBoxLayout()


        import_layout.setSpacing(
            10
        )


        import_layout.addWidget(
            self.drop_area,
            2
        )


        import_layout.addWidget(
            self.importer,
            1
        )



        self.drop_area.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )


        self.importer.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )



        # =====================
        # IMAGE LIST
        # =====================


        self.image_list = ImageListWidget()



        # =====================
        # PREVIEW
        # =====================


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
        # CONVERT OPTIONS
        # =====================


        settings_box = QFrame()


        settings_layout = QVBoxLayout(
            settings_box
        )


        settings_layout.setSpacing(
            10
        )



        settings_layout.addWidget(
            QLabel(
                "Conversion Settings"
            )
        )



        settings_layout.addWidget(
            QLabel(
                "Target Format"
            )
        )



        self.format_box = QComboBox()



        self.format_box.addItems(
            [
                "JPEG",
                "PNG",
                "WEBP",
                "AVIF",
                "GIF",
                "BMP",
                "TIFF",
                "HEIC",
                "HEIF",
                "ICO",
                "SVG",
            ]
        )



        settings_layout.addWidget(
            self.format_box
        )



        settings_layout.addWidget(
            QLabel(
                "Format Options"
            )
        )



        self.format_options = FormatOptionsPanel()



        settings_layout.addWidget(
            self.format_options
        )



        # =====================
        # OUTPUT
        # =====================


        self.output_selector = OutputSelector()


        self.output_folder = (
            self.output_selector.get_output_folder()
        )



        # =====================
        # ACTION
        # =====================


        self.start_button = QPushButton(
            "Start Conversion"
        )


        self.progress = ExportProgress()



        self.cancel_button = QPushButton(
            "Cancel Processing"
        )


        self.cancel_button.hide()



        # =====================
        # MAIN LAYOUT
        # =====================


        self.layout.addWidget(
            title
        )


        self.layout.addWidget(
            self.format_support
        )


        self.layout.addLayout(
            import_layout,
            1
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





    def connect_events(self):


        self.importer.images_added.connect(
            self.load_images
        )


        self.image_list.image_selected.connect(
            self.show_preview
        )


        self.output_selector.output_changed.connect(
            self.set_output_folder
        )


        self.format_box.currentTextChanged.connect(
            self.change_format
        )


        self.format_options.settings_changed.connect(
            self.update_format_settings
        )


        self.start_button.clicked.connect(
            self.start_convert
        )


        self.cancel_button.clicked.connect(
            self.cancel_processing
        )


        self.batch_service.progress_changed.connect(
            self.progress.update_progress
        )


        self.batch_service.processing_finished.connect(
            self.convert_finished
        )


        self.batch_service.processing_error.connect(
            self.convert_error
        )





    def change_format(
        self,
        format_name
    ):


        self.format_options.set_format(
            format_name
        )


        self.format_options.reset()



    def update_format_settings(
        self,
        settings
    ):

        self.format_settings = settings





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


        return {

            "operations": [],

            "output": {

                "format":
                    self.format_box.currentText(),

                "options":
                    self.format_settings
            }

        }





    def start_convert(
        self
    ):


        if not self.images:

            QMessageBox.warning(
                self,
                "Convert",
                "No images selected"
            )

            return



        if not self.output_folder:

            QMessageBox.warning(
                self,
                "Convert",
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
                "Conversion Error",
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





    def convert_finished(
        self,
        result
    ):


        self.start_button.setEnabled(
            True
        )


        self.cancel_button.hide()


        self.progress.finished()





    def convert_error(
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