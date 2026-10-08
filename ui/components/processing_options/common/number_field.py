"""Reusable, styled integer input consistent with DropdownField/SliderField."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel, QSpinBox, QVBoxLayout, QWidget


class NumberField(QWidget):
    value_changed = Signal(int)

    def __init__(
        self, title, minimum=0, maximum=100000, default=0, suffix="", parent=None
    ):
        super().__init__(parent)
        self.setObjectName("number_field")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(9)
        self.label = QLabel(str(title))
        self.label.setObjectName("number_field_label")
        self.label.setWordWrap(True)
        self.spin = QSpinBox(self)
        self.spin.setObjectName("premium_number_input")
        self.spin.setRange(int(minimum), int(maximum))
        self.spin.setSuffix(str(suffix))
        self.spin.setValue(int(default))
        self.spin.setMinimumHeight(44)
        self.spin.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.spin.setAccessibleName(str(title))
        self.label.setBuddy(self.spin)
        layout.addWidget(self.label)
        layout.addWidget(self.spin)
        self.spin.valueChanged.connect(self.value_changed.emit)
        self.apply_styles()

    def value(self):
        return self.spin.value()

    def set_value(self, value):
        self.spin.setValue(int(value))

    def set_range(self, minimum, maximum):
        self.spin.setRange(int(minimum), int(maximum))

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget#number_field { background: transparent; border: none; }
            QLabel#number_field_label {
                color: #CBD5E1; background: transparent; border: none;
                font-family: 'Segoe UI'; font-size: 12px; font-weight: 600;
            }
            QLabel#number_field_label:disabled { color: #64748B; }
            QSpinBox#premium_number_input {
                background-color: #1B2940; color: #F1F5F9;
                border: 1px solid #304259; border-radius: 10px;
                padding: 8px 13px; font-family: 'Segoe UI';
                font-size: 12px; font-weight: 600;
                selection-background-color: #173A40;
                selection-color: #5EEAD4;
            }
            QSpinBox#premium_number_input:hover { background-color: #203149; border-color: #426273; }
            QSpinBox#premium_number_input:focus { border-color: #5EEAD4; }
            QSpinBox#premium_number_input:disabled {
                background-color: #151E2D; color: #64748B; border-color: #253348;
            }
            QSpinBox#premium_number_input::up-button,
            QSpinBox#premium_number_input::down-button {
                background-color: #263449; border: none; width: 22px;
            }
            QSpinBox#premium_number_input::up-button:hover,
            QSpinBox#premium_number_input::down-button:hover { background-color: #173A40; }
        """)
