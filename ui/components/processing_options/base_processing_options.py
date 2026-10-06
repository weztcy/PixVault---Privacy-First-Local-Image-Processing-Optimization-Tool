from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel
)


from PySide6.QtCore import (
    Signal
)







class BaseProcessingOptions(QWidget):


    settings_changed = Signal(
        dict
    )


    validation_changed = Signal(
        bool,
        str
    )






    def __init__(
        self
    ):


        super().__init__()


        self.current_format = None


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


        self.warning_label = QLabel()


        self.warning_label.setWordWrap(
            True
        )


        self.warning_label.hide()



        self.layout.addWidget(
            self.warning_label
        )








    def add_widget(
        self,
        widget
    ):


        self.layout.addWidget(
            widget
        )









    def set_format(
        self,
        format_name
    ):


        """
        Dipanggil ketika output format berubah.

        Contoh:

        JPEG:
            BitDepth16 disable

        WEBP:
            CMYK disable

        """


        self.current_format = (

            str(
                format_name
            ).upper()

        )


        self.update_capability()



    def update_capability(
        self
    ):


        """
        Override oleh child.

        Digunakan untuk:
        - disable widget
        - warning
        - hide option

        """


        pass







    def show_warning(
        self,
        message
    ):


        if message:


            self.warning_label.setText(

                "⚠ " + message

            )


            self.warning_label.show()



        else:


            self.warning_label.clear()


            self.warning_label.hide()








    def emit_settings(
        self
    ):


        self.settings_changed.emit(

            self.get_settings()

        )








    def get_settings(
        self
    ):


        """
        Semua child wajib override.

        Return:

        {
            "type":"resize",
            "method":"width",
            ...
        }

        """


        return {}








    def reset(
        self
    ):


        """
        Semua child override
        jika memiliki default value.
        """


        pass








    def validate(
        self
    ):


        """
        Return:

        (
            True,
            ""
        )


        atau


        (
            False,
            "Error message"
        )

        """


        return (

            True,

            ""

        )







    def set_defaults(
        self,
        settings
    ):


        """
        Untuk load saved preset/history.

        Contoh:

        {
            "method":"width",
            "value":1200
        }

        """


        pass