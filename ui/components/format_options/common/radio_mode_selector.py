from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QRadioButton,
    QVBoxLayout,
    QButtonGroup
)


from PySide6.QtCore import Signal





class RadioModeSelector(QWidget):


    mode_changed = Signal(
        str
    )





    def __init__(
        self,
        title,
        modes,
        default=None
    ):

        super().__init__()



        self.buttons = {}



        layout = QVBoxLayout(

            self

        )


        layout.addWidget(

            QLabel(

                title

            )

        )



        self.group = QButtonGroup(

            self

        )



        for mode in modes:


            button = QRadioButton(

                mode

            )


            self.buttons[mode] = button



            self.group.addButton(

                button

            )



            layout.addWidget(

                button

            )


            button.toggled.connect(

                lambda checked,
                value=mode:

                self.changed(

                    checked,

                    value

                )

            )



        if default and default in self.buttons:


            self.buttons[default].setChecked(

                True

            )









    def changed(
        self,
        checked,
        mode
    ):


        if checked:


            self.mode_changed.emit(

                mode

            )








    def value(
        self
    ):


        for name, button in self.buttons.items():


            if button.isChecked():

                return name



        return None







    def set_value(
        self,
        value
    ):


        if value in self.buttons:


            self.buttons[value].setChecked(

                True

            )