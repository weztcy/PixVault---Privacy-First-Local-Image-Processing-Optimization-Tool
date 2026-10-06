from PySide6.QtWidgets import (
    QLabel,
    QComboBox,
    QCheckBox
)


from ui.components.processing_options.base_processing_options import (
    BaseProcessingOptions
)







class MetadataOptions(
    BaseProcessingOptions
):


    METADATA_TYPES = [

        "EXIF",

        "GPS Location",

        "IPTC",

        "XMP",

        "ICC Profile",

        "Maker Notes",

        "Software Information",

        "Copyright Information"

    ]







    def __init__(
        self
    ):

        super().__init__()







    def setup_ui(
        self
    ):


        super().setup_ui()



        # =====================
        # MODE
        # =====================


        self.add_widget(

            QLabel(
                "Metadata Removal Mode"
            )

        )


        self.mode = QComboBox()


        self.mode.addItems(

            [

                "Remove All Metadata",

                "Custom"

            ]

        )


        self.add_widget(

            self.mode

        )






        # =====================
        # CUSTOM OPTIONS
        # =====================


        self.checkboxes = {}



        self.add_widget(

            QLabel(
                "Metadata Types"
            )

        )



        for item in self.METADATA_TYPES:


            checkbox = QCheckBox(

                item

            )


            checkbox.setChecked(

                True

            )


            self.checkboxes[item] = checkbox


            self.add_widget(

                checkbox

            )



        self.mode.currentTextChanged.connect(

            self.update_ui

        )


        self.update_ui()







    def update_ui(
        self
    ):


        custom = (

            self.mode.currentText()

            ==

            "Custom"

        )



        for checkbox in self.checkboxes.values():


            checkbox.setVisible(

                custom

            )









    def get_settings(
        self
    ):


        if self.mode.currentText() == "Remove All Metadata":


            return {


                "type":

                    "metadata",


                "mode":

                    "all"

            }





        remove = []



        for name, checkbox in self.checkboxes.items():


            if checkbox.isChecked():


                remove.append(

                    name

                )



        return {


            "type":

                "metadata",


            "mode":

                "custom",


            "remove":

                remove

        }









    def reset(
        self
    ):


        self.mode.setCurrentText(

            "Remove All Metadata"

        )


        for checkbox in self.checkboxes.values():


            checkbox.setChecked(

                True

            )


        self.update_ui()







    def update_capability(
        self
    ):


        if self.current_format == "SVG":


            self.show_warning(

                "SVG uses XML metadata instead of EXIF metadata."

            )


        else:


            self.show_warning(

                ""

            )