from PySide6.QtWidgets import (
    QStackedWidget,
    QScrollArea,
    QWidget
)


from ui.pages.home_page import HomePage
from ui.pages.all_processing_page import AllProcessingPage


from ui.pages.convert_page import ConvertPage
from ui.pages.compress_page import CompressPage
from ui.pages.resize_page import ResizePage
from ui.pages.crop_page import CropPage
from ui.pages.transform_page import TransformPage
from ui.pages.dpi_page import DPIPage
from ui.pages.metadata_page import MetadataPage
from ui.pages.colorspace_page import ColorSpacePage
from ui.pages.bitdepth_page import BitDepthPage


from ui.pages.history_page import HistoryPage
from ui.pages.settings_page import SettingsPage
from ui.pages.privacy_page import PrivacyPage




class Workspace(QStackedWidget):


    def __init__(
        self,
        image_service,
        batch_service,
        history_service
    ):

        super().__init__()


        self.image_service = image_service

        self.batch_service = batch_service

        self.history_service = history_service


        self.pages = {}


        self.setup_pages()



    def setup_pages(
        self
    ):


        self.register_main_pages()


        self.register_tool_pages()


        self.register_system_pages()


        self.show_page(
            "home"
        )



    def wrap_page(
        self,
        widget
    ):


        scroll = QScrollArea()


        scroll.setWidgetResizable(
            True
        )


        scroll.setFrameShape(
            QScrollArea.NoFrame
        )


        scroll.setWidget(
            widget
        )


        return scroll



    def register_main_pages(
        self
    ):


        self.add_page(
            "home",
            HomePage()
        )


        self.add_page(
            "all_processing",
            AllProcessingPage(
                self.image_service,
                self.batch_service
            )
        )



    def register_tool_pages(
        self
    ):


        tools = {


            "convert":
                ConvertPage(
                    self.image_service
                ),


            "compress":
                CompressPage(
                    self.image_service
                ),


            "resize":
                ResizePage(
                    self.image_service
                ),


            "crop":
                CropPage(
                    self.image_service
                ),


            "transform":
                TransformPage(
                    self.image_service
                ),


            "dpi":
                DPIPage(
                    self.image_service
                ),


            "metadata":
                MetadataPage(
                    self.image_service
                ),


            "colorspace":
                ColorSpacePage(
                    self.image_service
                ),


            "bitdepth":
                BitDepthPage(
                    self.image_service
                )

        }



        for name, page in tools.items():


            self.add_page(
                name,
                page
            )



    def register_system_pages(
        self
    ):


        self.add_page(
            "history",
            HistoryPage(
                self.history_service
            )
        )


        self.add_page(
            "settings",
            SettingsPage()
        )


        self.add_page(
            "privacy",
            PrivacyPage()
        )



    def add_page(
        self,
        name,
        widget
    ):


        if name in self.pages:

            return



        scroll_page = self.wrap_page(
            widget
        )


        self.pages[name] = scroll_page


        self.addWidget(
            scroll_page
        )



    def show_page(
        self,
        name
    ):


        page = self.pages.get(
            name
        )


        if page:

            self.setCurrentWidget(
                page
            )



    def get_page(
        self,
        name
    ):


        return self.pages.get(
            name
        )