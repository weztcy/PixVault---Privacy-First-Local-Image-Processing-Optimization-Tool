from PySide6.QtWidgets import (
    QLabel,
    QComboBox,
    QSpinBox
)


from ui.components.processing_options.base_processing_options import (
    BaseProcessingOptions
)







class CropOptions(
    BaseProcessingOptions
):


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
                "Crop Mode"
            )
        )


        self.mode = QComboBox()


        self.mode.addItems(

            [

                "Aspect Ratio",

                "Fixed Dimensions",

                "Percentage",

                "Custom Coordinates"

            ]

        )


        self.add_widget(

            self.mode

        )





        # =====================
        # ASPECT RATIO
        # =====================


        self.ratio_label = QLabel(
            "Aspect Ratio"
        )


        self.ratio = QComboBox()


        self.ratio.addItems(

            [

                "1:1",

                "4:3",

                "16:9",

                "3:2",

                "21:9"

            ]

        )


        self.add_widget(

            self.ratio_label

        )


        self.add_widget(

            self.ratio

        )





        # =====================
        # WIDTH HEIGHT
        # =====================


        self.width_label = QLabel(
            "Width"
        )


        self.width = QSpinBox()


        self.width.setRange(
            1,
            100000
        )



        self.height_label = QLabel(
            "Height"
        )


        self.height = QSpinBox()


        self.height.setRange(
            1,
            100000
        )



        self.add_widget(
            self.width_label
        )


        self.add_widget(
            self.width
        )


        self.add_widget(
            self.height_label
        )


        self.add_widget(
            self.height
        )






        # =====================
        # PERCENTAGE
        # =====================


        self.percentage_label = QLabel(
            "Percentage (%)"
        )


        self.percentage = QSpinBox()


        self.percentage.setRange(
            1,
            100
        )


        self.percentage.setValue(
            100
        )


        self.add_widget(

            self.percentage_label

        )


        self.add_widget(

            self.percentage

        )







        # =====================
        # COORDINATES
        # =====================


        self.x_label = QLabel(
            "X"
        )


        self.x = QSpinBox()


        self.y_label = QLabel(
            "Y"
        )


        self.y = QSpinBox()



        self.x.setRange(
            0,
            100000
        )


        self.y.setRange(
            0,
            100000
        )



        self.add_widget(
            self.x_label
        )


        self.add_widget(
            self.x
        )


        self.add_widget(
            self.y_label
        )


        self.add_widget(
            self.y
        )





        self.mode.currentTextChanged.connect(

            self.update_ui

        )


        self.update_ui()







    def update_ui(
        self
    ):


        mode = self.mode.currentText()



        aspect = (
            mode == "Aspect Ratio"
        )


        fixed = (
            mode == "Fixed Dimensions"
        )


        percentage = (
            mode == "Percentage"
        )


        coordinates = (
            mode == "Custom Coordinates"
        )




        self.ratio_label.setVisible(
            aspect
        )

        self.ratio.setVisible(
            aspect
        )




        self.width_label.setVisible(
            fixed or coordinates
        )


        self.width.setVisible(
            fixed or coordinates
        )


        self.height_label.setVisible(
            fixed or coordinates
        )


        self.height.setVisible(
            fixed or coordinates
        )




        self.percentage_label.setVisible(
            percentage
        )


        self.percentage.setVisible(
            percentage
        )




        self.x_label.setVisible(
            coordinates
        )


        self.x.setVisible(
            coordinates
        )


        self.y_label.setVisible(
            coordinates
        )


        self.y.setVisible(
            coordinates
        )









    def get_settings(
        self
    ):


        mode_map = {


            "Aspect Ratio":
                "aspect_ratio",


            "Fixed Dimensions":
                "fixed",


            "Percentage":
                "percentage",


            "Custom Coordinates":
                "coordinates"

        }



        settings = {


            "type":
                "crop",


            "mode":
                mode_map[
                    self.mode.currentText()
                ]

        }




        mode = settings["mode"]




        if mode == "aspect_ratio":


            settings["ratio"] = (

                self.ratio.currentText()

            )



        elif mode == "fixed":


            settings["width"] = (

                self.width.value()

            )


            settings["height"] = (

                self.height.value()

            )



        elif mode == "percentage":


            settings["value"] = (

                self.percentage.value()

            )



        elif mode == "coordinates":


            settings["x"] = (

                self.x.value()

            )


            settings["y"] = (

                self.y.value()

            )


            settings["width"] = (

                self.width.value()

            )


            settings["height"] = (

                self.height.value()

            )



        return settings







    def reset(
        self
    ):


        self.mode.setCurrentText(

            "Aspect Ratio"

        )


        self.ratio.setCurrentText(

            "1:1"

        )


        self.width.setValue(

            1000

        )


        self.height.setValue(

            1000

        )


        self.percentage.setValue(

            100

        )


        self.x.setValue(

            0

        )


        self.y.setValue(

            0

        )


        self.update_ui()







    def update_capability(
        self
    ):


        if self.current_format == "SVG":


            self.show_warning(

                "SVG crop requires vector clipping support."

            )


        else:


            self.show_warning(

                ""

            )