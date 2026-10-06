from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSlider, QVBoxLayout, QWidget


class ValueSlider(QWidget):
    value_changed = Signal(int)

    def __init__(self, title, minimum, maximum, value=None, parent=None):

        super().__init__(parent)

        self.minimum = minimum

        self.maximum = maximum

        self.default_value = value if value is not None else minimum

        self.setup_ui(title)

        self.set_value(self.default_value)

    def setup_ui(self, title):

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setSpacing(4)

        header = QHBoxLayout()

        self.title_label = QLabel(title)

        self.value_label = QLabel("0")

        header.addWidget(self.title_label)

        header.addStretch()

        header.addWidget(self.value_label)

        self.main_layout.addLayout(header)

        self.slider = QSlider(Qt.Orientation.Horizontal)

        self.slider.setRange(self.minimum, self.maximum)

        self.slider.valueChanged.connect(self.on_value_changed)

        self.main_layout.addWidget(self.slider)

    def on_value_changed(self, value):

        self.value_label.setText(str(value))

        self.value_changed.emit(value)

    def value(self):

        return self.slider.value()

    def set_value(self, value):

        self.slider.setValue(value)

        self.value_label.setText(str(value))

    def reset(self):

        self.set_value(self.default_value)

    def set_range(self, minimum, maximum):

        self.minimum = minimum

        self.maximum = maximum

        self.slider.setRange(minimum, maximum)
