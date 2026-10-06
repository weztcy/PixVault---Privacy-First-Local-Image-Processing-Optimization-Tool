from PySide6.QtWidgets import (
    QLabel,
    QComboBox
)


from ui.components.processing_options.base_processing_options import (
    BaseProcessingOptions
)







class ColorSpaceOptions(
    BaseProcessingOptions
):


    COLOR_SPACES = [

        "sRGB",

        "Adobe RGB",

        "Display P3",

        "CMYK",

        "Grayscale"

    ]



    RENDERING_INTENTS = [

        "Perceptual",

        "Relative Colorimetric",

        "Saturation",

        "Absolute Colorimetric"

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
        # COLOR SPACE
        # =====================


        self.add_widget(

            QLabel(
                "Color Space"
            )

        )


        self.color_space = QComboBox()


        self.color_space.addItems(

            self.COLOR_SPACES

        )


        self.color_space.setCurrentText(

            "sRGB"

        )


        self.add_widget(

            self.color_space

        )






        # =====================
        # RENDERING INTENT
        # =====================


        self.intent_label = QLabel(

            "Rendering Intent"

        )


        self.intent = QComboBox()


        self.intent.addItems(

            self.RENDERING_INTENTS

        )


        self.intent.setCurrentText(

            "Perceptual"

        )


        self.add_widget(

            self.intent_label

        )


        self.add_widget(

            self.intent

        )



        self.color_space.currentTextChanged.connect(

            self.update_ui

        )


        self.update_ui()







    def update_ui(
        self
    ):


        grayscale = (

            self.color_space.currentText()

            ==

            "Grayscale"

        )


        self.intent.setEnabled(

            not grayscale

        )


        self.intent_label.setEnabled(

            not grayscale

        )









    def get_settings(
        self
    ):


        return {


            "type":

                "colorspace",


            "target":

                self.color_space.currentText(),



            "rendering_intent":

                self.intent.currentText()

                if self.intent.isEnabled()

                else None

        }









    def reset(
        self
    ):


        self.color_space.setCurrentText(

            "sRGB"

        )


        self.intent.setCurrentText(

            "Perceptual"

        )


        self.update_ui()







    def update_capability(
        self
    ):


        unsupported = {}



        if self.current_format == "WEBP":


            unsupported = {

                "Adobe RGB",

                "Display P3",

                "CMYK"

            }



        elif self.current_format == "GIF":


            unsupported = {

                "Adobe RGB",

                "Display P3",

                "CMYK"

            }



        elif self.current_format in [

            "BMP",

            "ICO"

        ]:


            unsupported = {

                "Adobe RGB",

                "Display P3",

                "CMYK"

            }



        elif self.current_format in [

            "PNG"

        ]:


            unsupported = {

                "CMYK"

            }



        elif self.current_format in [

            "AVIF"

        ]:


            unsupported = {

                "CMYK"

            }



        elif self.current_format in [

            "HEIC",

            "HEIF"

        ]:


            unsupported = {

                "CMYK"

            }



        for index in range(

            self.color_space.count()

        ):


            item = self.color_space.itemText(

                index

            )


            enabled = item not in unsupported


            self.color_space.model().item(

                index

            ).setEnabled(

                enabled

            )



        if self.color_space.currentText() in unsupported:


            self.color_space.setCurrentText(

                "sRGB"

            )



        if unsupported:


            self.show_warning(

                f"{self.current_format} has limited color space support."

            )


        else:


            self.show_warning(

                ""

            )