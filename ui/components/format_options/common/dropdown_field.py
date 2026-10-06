from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWidget


class DropdownField(QWidget):
    value_changed = Signal(str)

    def __init__(self, title, items, default=None):

        super().__init__()

        layout = QVBoxLayout(self)

        layout.setSpacing(5)

        self.label = QLabel(title)

        layout.addWidget(self.label)

        self.combo = QComboBox()

        self.combo.addItems(items)

        if default:
            self.combo.setCurrentText(default)

        self.combo.currentTextChanged.connect(self.value_changed.emit)

        layout.addWidget(self.combo)

    def value(self):

        return self.combo.currentText()

    def set_value(self, value):

        self.combo.setCurrentText(value)
