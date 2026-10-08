from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)


class CheckboxField(QWidget):
    value_changed = Signal(bool)

    def __init__(self, text, default=False):
        super().__init__()

        self.setObjectName("checkbox_field")

        self.setup_ui(text, default)
        self.apply_styles()

    # =====================
    # USER INTERFACE
    # =====================

    def setup_ui(self, text, default):
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # =====================
        # CHECKBOX CONTAINER
        # =====================

        self.container = QFrame()
        self.container.setObjectName("checkbox_field_container")

        self.container.setMinimumHeight(44)

        container_layout = QHBoxLayout(self.container)

        container_layout.setContentsMargins(14, 8, 14, 8)

        container_layout.setSpacing(10)

        # =====================
        # CHECKBOX
        # =====================

        self.checkbox = QCheckBox(text)

        self.checkbox.setObjectName("premium_checkbox")

        self.checkbox.setCursor(Qt.CursorShape.PointingHandCursor)

        self.checkbox.setChecked(bool(default))

        self.checkbox.setMinimumHeight(26)

        self.checkbox.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        container_layout.addWidget(
            self.checkbox,
            1,
        )

        main_layout.addWidget(self.container)

        # =====================
        # SIGNAL CONNECTION
        # =====================

        self.checkbox.toggled.connect(self.changed)

    # =====================
    # VALUE CHANGED
    # =====================

    def changed(self, checked=None):
        self.value_changed.emit(self.checkbox.isChecked())

    # =====================
    # GET VALUE
    # =====================

    def value(self):
        return self.checkbox.isChecked()

    # =====================
    # SET VALUE
    # =====================

    def set_value(self, value):
        self.checkbox.setChecked(bool(value))

    # =====================
    # PREMIUM STYLING
    # =====================

    def apply_styles(self):
        self.setStyleSheet(
            """
            /* =========================
               FIELD CONTAINER
            ========================= */

            QFrame#checkbox_field_container {
                background-color: #1b2940;
                border: 1px solid #304259;
                border-radius: 10px;
            }

            QFrame#checkbox_field_container:hover {
                background-color: #203149;
                border: 1px solid #426273;
            }

            /* =========================
               CHECKBOX TEXT
            ========================= */

            QCheckBox#premium_checkbox {
                background: transparent;
                border: none;

                color: #d5deea;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 500;

                spacing: 12px;
            }

            QCheckBox#premium_checkbox:hover {
                color: #f8fafc;
            }

            /* =========================
               UNCHECKED INDICATOR
            ========================= */

            QCheckBox#premium_checkbox::indicator {
                width: 18px;
                height: 18px;

                background-color: #101b2d;

                border: 1px solid #50647c;
                border-radius: 5px;
            }

            /* =========================
               INDICATOR HOVER
            ========================= */

            QCheckBox#premium_checkbox::indicator:hover {
                background-color: #263b4d;
                border: 1px solid #5eead4;
            }

            /* =========================
               CHECKED INDICATOR
            ========================= */

            QCheckBox#premium_checkbox::indicator:checked {
                background-color: #5eead4;
                border: 1px solid #5eead4;
                border-radius: 5px;
            }

            QCheckBox#premium_checkbox::indicator:checked:hover {
                background-color: #99f6e4;
                border: 1px solid #99f6e4;
            }

            /* =========================
               DISABLED STATE
            ========================= */

            QFrame#checkbox_field_container:disabled {
                background-color: #151e2d;
                border: 1px solid #253348;
            }

            QCheckBox#premium_checkbox:disabled {
                color: #64748b;
            }

            QCheckBox#premium_checkbox::indicator:disabled {
                background-color: #202b3b;
                border: 1px solid #354459;
            }

            /* =========================
               KEYBOARD FOCUS
            ========================= */

            QCheckBox#premium_checkbox::indicator:focus {
                border: 2px solid #5eead4;
            }
            """
        )
