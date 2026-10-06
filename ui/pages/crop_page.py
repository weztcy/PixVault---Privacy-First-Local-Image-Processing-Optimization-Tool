from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QFrame,
    QMessageBox
)


from ui.components.image_importer import ImageImporter
from ui.components.image_list_widget import ImageListWidget
from ui.components.image_preview import ImagePreview
from ui.components.image_info_panel import ImageInfoPanel
from ui.components.output_selector import OutputSelector
from ui.components.export_progress import ExportProgress


from ui.components.processing_options.crop_options import (
    CropOptions
)







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









        # =====================
        # CROP OPTIONS
        # =====================


        crop_box = QFrame()



        crop_layout = QVBoxLayout(
            crop_box
        )



        crop_layout.addWidget(

            QLabel(
                "Crop Settings"
            )

        )



        self.crop_options = CropOptions()



        crop_layout.addWidget(

            self.crop_options

        )









        self.output_selector = OutputSelector()



        self.output_folder = (

            self.output_selector.get_output_folder()

        )





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



        self.batch_service.progress_changed.connect(

            self.progress.update_progress

        )



        self.batch_service.processing_finished.connect(

            self.crop_finished

        )



        self.batch_service.processing_error.connect(

            self.crop_error

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


        operation = (

            self.crop_options.get_settings()

        )



        operation["type"] = (

            "crop"

        )



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
        