from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout
)





class BaseFormatOptions(QWidget):


    def __init__(
        self
    ):

        super().__init__()


        self.setup_ui()







    def setup_ui(
        self
    ):


        self.layout = QVBoxLayout(
            self
        )


        self.layout.setSpacing(
            10
        )







    def add_widget(
        self,
        widget
    ):


        self.layout.addWidget(
            widget
        )







    def get_settings(
        self
    ):


        """
        Return format specific encoder settings.

        Must be overridden by child class.

        Example:

        {
            "quality":85,
            "progressive":True
        }

        """


        return {}







    def reset(
        self
    ):


        """
        Reset all widgets to default value.

        Override if format needs reset logic.
        """


        pass







    def set_defaults(
        self
    ):


        """
        Optional method.

        Used when loading saved settings.
        """


        pass