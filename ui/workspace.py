from PySide6.QtWidgets import QStackedWidget

from ui.pages.home_page import HomePage
from ui.pages.all_processing_page import AllProcessingPage
from ui.pages.history_page import HistoryPage
from ui.pages.settings_page import SettingsPage
from ui.pages.privacy_page import PrivacyPage


class Workspace(QStackedWidget):

    def __init__(self):
        super().__init__()

        self.pages = {}

        self.setup_pages()


    def setup_pages(self):

        self.add_page(
            "home",
            HomePage()
        )

        self.add_page(
            "all_processing",
            AllProcessingPage()
        )

        self.add_page(
            "history",
            HistoryPage()
        )

        self.add_page(
            "settings",
            SettingsPage()
        )

        self.add_page(
            "privacy",
            PrivacyPage()
        )


        self.show_page("home")


    def add_page(self, name, widget):

        self.pages[name] = widget

        self.addWidget(widget)


    def show_page(self, name):

        if name in self.pages:

            self.setCurrentWidget(
                self.pages[name]
            )