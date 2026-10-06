from PySide6.QtWidgets import (
    QLabel,
    QComboBox,
    QSpinBox
)


from ui.components.processing_options.base_processing_options import (
    BaseProcessingOptions
)







class TransformOptions(
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
        # ROTATION
        # =====================


        self.add_widget(

            QLabel(
                "Rotation"
            )

        )


        self.rotation = QComboBox()


        self.rotation.addItems(

            [

                "None",

                "90° Clockwise",

                "180°",

                "90° Counterclockwise",

                "Custom Angle"

            ]

        )


        self.add_widget(

            self.rotation

        )






        # =====================
        # CUSTOM ANGLE
        # =====================


        self.angle_label = QLabel(
            "Custom Angle"
        )


        self.angle = QSpinBox()


        self.angle.setRange(
            -360,
            360
        )


        self.angle.setValue(
            0
        )



        self.add_widget(

            self.angle_label

        )


        self.add_widget(

            self.angle

        )







        # =====================
        # FLIP
        # =====================


        self.add_widget(

            QLabel(
                "Flip"
            )

        )


        self.flip = QComboBox()


        self.flip.addItems(

            [

                "None",

                "Horizontal",

                "Vertical",

                "Both"

            ]

        )


        self.add_widget(

            self.flip

        )





        self.rotation.currentTextChanged.connect(

            self.update_ui

        )


        self.update_ui()







    def update_ui(
        self
    ):


        custom = (

            self.rotation.currentText()

            ==

            "Custom Angle"

        )


        self.angle_label.setVisible(

            custom

        )


        self.angle.setVisible(

            custom

        )








    def get_settings(
        self
    ):


        rotation_map = {


            "None":
                "none",


            "90° Clockwise":
                90,


            "180°":
                180,


            "90° Counterclockwise":
                -90,


            "Custom Angle":
                self.angle.value()

        }



        flip_map = {


            "None":
                "none",


            "Horizontal":
                "horizontal",


            "Vertical":
                "vertical",


            "Both":
                "both"

        }



        return {


            "type":
                "transform",


            "rotation":
                rotation_map[

                    self.rotation.currentText()

                ],


            "flip":
                flip_map[

                    self.flip.currentText()

                ]

        }







    def reset(
        self
    ):


        self.rotation.setCurrentText(

            "None"

        )


        self.angle.setValue(

            0

        )


        self.flip.setCurrentText(

            "None"

        )


        self.update_ui()







    def update_capability(
        self
    ):


        if self.current_format == "SVG":


            self.show_warning(

                "SVG uses vector transform instead of pixel transform."

            )


        else:


            self.show_warning(

                ""

            )