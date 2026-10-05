from PySide6.QtWidgets import QStackedWidget


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


        # MAIN

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



        # TOOLS


        self.add_page(
            "convert",
            ConvertPage(
                self.image_service
            )
        )


        self.add_page(
            "compress",
            CompressPage(
                self.image_service
            )
        )


        self.add_page(
            "resize",
            ResizePage(
                self.image_service
            )
        )


        self.add_page(
            "crop",
            CropPage(
                self.image_service
            )
        )


        self.add_page(
            "transform",
            TransformPage(
                self.image_service
            )
        )


        self.add_page(
            "dpi",
            DPIPage(
                self.image_service
            )
        )


        self.add_page(
            "metadata",
            MetadataPage(
                self.image_service
            )
        )


        self.add_page(
            "colorspace",
            ColorSpacePage(
                self.image_service
            )
        )


        self.add_page(
            "bitdepth",
            BitDepthPage(
                self.image_service
            )
        )



        # MANAGEMENT


        self.add_page(
            "history",
            HistoryPage(
                self.history_service
            )
        )



        # SYSTEM


        self.add_page(
            "settings",
            SettingsPage()
        )


        self.add_page(
            "privacy",
            PrivacyPage()
        )



        self.show_page(
            "home"
        )



    def add_page(
        self,
        name,
        widget
    ):


        self.pages[name] = widget


        self.addWidget(
            widget
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