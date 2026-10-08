from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QLabel,
    QRadioButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class RadioModeSelector(QWidget):
    mode_changed = Signal(str)

    def __init__(
        self,
        title,
        modes,
        default=None,
    ):
        super().__init__()

        self.setObjectName("radio_mode_selector")

        self.buttons = {}
        self.group = QButtonGroup(self)
        self.group.setExclusive(True)

        self.setup_ui(
            title,
            modes,
            default,
        )

        self.apply_styles()

    # =====================
    # USER INTERFACE
    # =====================

    def setup_ui(
        self,
        title,
        modes,
        default,
    ):
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.setSpacing(10)

        # =====================
        # SECTION TITLE
        # =====================

        self.title_label = QLabel(title)

        self.title_label.setObjectName("radio_selector_title")

        self.title_label.setWordWrap(True)

        main_layout.addWidget(self.title_label)

        main_layout.addSpacing(3)

        # =====================
        # RADIO OPTIONS
        # =====================

        self.options_layout = QVBoxLayout()

        self.options_layout.setSpacing(8)

        self.options_layout.setContentsMargins(0, 0, 0, 0)

        for mode in modes:
            button = self.create_radio_option(mode)

            self.buttons[mode] = button

            self.group.addButton(button)

            self.options_layout.addWidget(button)

            button.toggled.connect(
                lambda checked, value=mode: self.changed(checked, value)
            )

        main_layout.addLayout(self.options_layout)

        # =====================
        # DEFAULT SELECTION
        # =====================

        if default is not None and default in self.buttons:
            self.buttons[default].setChecked(True)

    # =====================
    # RADIO OPTION FACTORY
    # =====================

    def create_radio_option(self, mode):
        button = QRadioButton(str(mode))

        button.setObjectName("premium_radio_option")

        button.setMinimumHeight(48)

        button.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        button.setCursor(Qt.CursorShape.PointingHandCursor)

        button.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        button.setAccessibleName(str(mode))

        return button

    # =====================
    # MODE CHANGED
    # =====================

    def changed(
        self,
        checked,
        mode,
    ):
        if checked:
            self.mode_changed.emit(str(mode))

    # =====================
    # GET CURRENT VALUE
    # =====================

    def value(self):
        for name, button in self.buttons.items():
            if button.isChecked():
                return name

        return None

    # =====================
    # SET CURRENT VALUE
    # =====================

    def set_value(self, value):
        if value in self.buttons:
            self.buttons[value].setChecked(True)

    # =====================
    # PREMIUM STYLING
    # =====================

    def apply_styles(self):
        self.setStyleSheet(
            """
            /* =========================
               MAIN CONTAINER
            ========================= */

            QWidget#radio_mode_selector {
                background-color: transparent;
                border: none;
            }

            /* =========================
               SECTION TITLE
            ========================= */

            QLabel#radio_selector_title {
                color: #cbd5e1;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 600;

                background: transparent;
                border: none;
            }

            /* =========================
               RADIO OPTION CARD
            ========================= */

            QRadioButton#premium_radio_option {
                background-color: #1b2940;

                color: #d5deea;

                border: 1px solid #304259;
                border-radius: 10px;

                padding: 10px 14px;

                spacing: 12px;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 500;
            }

            /* =========================
               HOVER STATE
            ========================= */

            QRadioButton#premium_radio_option:hover {
                background-color: #203149;

                color: #f8fafc;

                border: 1px solid #426273;
            }

            /* =========================
               SELECTED STATE
            ========================= */

            QRadioButton#premium_radio_option:checked {
                background-color: #173a40;

                color: #5eead4;

                border: 1px solid #397d76;
                border-left: 3px solid #5eead4;

                font-weight: 700;
            }

            /* =========================
               SELECTED HOVER
            ========================= */

            QRadioButton#premium_radio_option:checked:hover {
                background-color: #1c4649;

                color: #99f6e4;

                border: 1px solid #5eead4;
                border-left: 3px solid #5eead4;
            }

            /* =========================
               RADIO INDICATOR
            ========================= */

            QRadioButton#premium_radio_option::indicator {
                width: 18px;
                height: 18px;

                background-color: #101b2d;

                border: 2px solid #50647c;
                border-radius: 11px;
            }

            /* =========================
               INDICATOR HOVER
            ========================= */

            QRadioButton#premium_radio_option::indicator:hover {
                border: 2px solid #5eead4;

                background-color: #203149;
            }

            /* =========================
               CHECKED INDICATOR
            ========================= */

            QRadioButton#premium_radio_option::indicator:checked {
                background-color: #5eead4;

                border: 5px solid #173a40;

                border-radius: 11px;
            }

            /* =========================
               CHECKED INDICATOR HOVER
            ========================= */

            QRadioButton#premium_radio_option::indicator:checked:hover {
                background-color: #99f6e4;

                border: 5px solid #1c4649;
            }

            /* =========================
               PRESSED STATE
            ========================= */

            QRadioButton#premium_radio_option:pressed {
                background-color: #244b52;
            }

            /* =========================
               KEYBOARD FOCUS
            ========================= */

            QRadioButton#premium_radio_option:focus {
                border: 1px solid #5eead4;
            }

            QRadioButton#premium_radio_option:checked:focus {
                border: 1px solid #5eead4;
                border-left: 3px solid #5eead4;
            }

            /* =========================
               DISABLED STATE
            ========================= */

            QRadioButton#premium_radio_option:disabled {
                background-color: #151e2d;

                color: #64748b;

                border: 1px solid #253348;
            }

            QRadioButton#premium_radio_option::indicator:disabled {
                background-color: #202b3b;

                border: 2px solid #354459;
            }

            /* =========================
               DISABLED SELECTED
            ========================= */

            QRadioButton#premium_radio_option:checked:disabled {
                background-color: #192c32;

                color: #6b9c98;

                border: 1px solid #294c4d;
            }
            """
        )
