from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QSlider,
    QVBoxLayout
)


from PySide6.QtCore import (
    Qt,
    Signal
)





class SliderField(QWidget):


    value_changed = Signal(
        int
    )





    def __init__(
        self,
        title,
        minimum,
        maximum,
        default
    ):

        super().__init__()


        self.title = title


        self.setup_ui(

            minimum,

            maximum,

            default

        )









    def setup_ui(
        self,
        minimum,
        maximum,
        default
    ):


        layout = QVBoxLayout(
            self
        )


        layout.setSpacing(
            5
        )



        self.label = QLabel(

            self.title

        )


        layout.addWidget(

            self.label

        )





        self.slider = QSlider(

            Qt.Orientation.Horizontal

        )


        self.slider.setRange(

            minimum,

            maximum

        )


        self.slider.setValue(

            default

        )


        self.slider.valueChanged.connect(

            self.update_value

        )


        layout.addWidget(

            self.slider

        )





        self.value_label = QLabel(

            str(default)

        )


        layout.addWidget(

            self.value_label

        )








    def update_value(
        self,
        value
    ):


        self.value_label.setText(

            str(value)

        )


        self.value_changed.emit(

            value

        )









    def value(
        self
    ):


        return self.slider.value()









    def set_value(
        self,
        value
    ):


        self.slider.setValue(

            value

        )