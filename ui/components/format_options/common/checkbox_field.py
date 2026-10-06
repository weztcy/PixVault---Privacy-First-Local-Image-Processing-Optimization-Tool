from PySide6.QtCore import Signal
from PySide6.QtWidgets import QCheckBox, QVBoxLayout, QWidget


class CheckboxField(QWidget):
    value_changed = Signal(bool)

    def __init__(self, text, default=False):

        super().__init__()

        self.checkbox = QCheckBox(text)

        self.checkbox.setChecked(default)

        self.checkbox.stateChanged.connect(self.changed)

        layout = QVBoxLayout(self)

        layout.addWidget(self.checkbox)

    def changed(self):

        self.value_changed.emit(self.checkbox.isChecked())

    def value(self):

        return self.checkbox.isChecked()

    def set_value(self, value):

        self.checkbox.setChecked(value)
