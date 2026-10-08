from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class OptionSection(QWidget):
    collapsed_changed = Signal(bool)

    def __init__(
        self,
        title,
        collapsible=True,
        parent=None,
    ):
        super().__init__(parent)

        self.title = title
        self.collapsible = collapsible
        self.collapsed = False

        self.setObjectName("option_section")

        self.setup_ui()
        self.apply_styles()

    # =====================
    # MAIN USER INTERFACE
    # =====================

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # =====================
        # PREMIUM SECTION CARD
        # =====================

        self.panel = QFrame()
        self.panel.setObjectName("option_section_panel")

        self.panel.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        self.panel_layout = QVBoxLayout(self.panel)

        self.panel_layout.setContentsMargins(1, 1, 1, 1)
        self.panel_layout.setSpacing(0)

        # =====================
        # SECTION HEADER
        # =====================

        self.header = QFrame()
        self.header.setObjectName("option_section_header")

        header_layout = QHBoxLayout(self.header)

        header_layout.setContentsMargins(14, 7, 14, 7)
        header_layout.setSpacing(12)

        # Emerald accent

        self.accent = QFrame()
        self.accent.setObjectName("option_section_accent")

        self.accent.setFixedSize(3, 23)

        header_layout.addWidget(
            self.accent,
            0,
            Qt.AlignmentFlag.AlignVCenter,
        )

        # =====================
        # COLLAPSIBLE HEADER
        # =====================

        if self.collapsible:
            self.toggle_button = QToolButton()

            self.toggle_button.setObjectName("option_section_toggle")

            self.toggle_button.setText(str(self.title))

            self.toggle_button.setCheckable(True)

            self.toggle_button.setChecked(True)

            self.toggle_button.setArrowType(Qt.ArrowType.DownArrow)

            self.toggle_button.setToolButtonStyle(
                Qt.ToolButtonStyle.ToolButtonTextBesideIcon
            )

            self.toggle_button.setAutoRaise(True)

            self.toggle_button.setMinimumHeight(36)

            self.toggle_button.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed,
            )

            self.toggle_button.setCursor(Qt.CursorShape.PointingHandCursor)

            self.toggle_button.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

            self.toggle_button.setAccessibleName(str(self.title))

            self.toggle_button.setToolTip("Expand or collapse this section")

            self.toggle_button.clicked.connect(self.toggle)

            header_layout.addWidget(
                self.toggle_button,
                1,
            )

        # =====================
        # NON-COLLAPSIBLE HEADER
        # =====================

        else:
            self.title_label = QLabel(str(self.title))

            self.title_label.setObjectName("option_section_title")

            self.title_label.setWordWrap(True)

            self.title_label.setMinimumHeight(36)

            self.title_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

            header_layout.addWidget(
                self.title_label,
                1,
            )

        self.panel_layout.addWidget(self.header)

        # =====================
        # HEADER DIVIDER
        # =====================

        self.divider = QFrame()

        self.divider.setObjectName("option_section_divider")

        self.divider.setFixedHeight(1)

        self.panel_layout.addWidget(self.divider)

        # =====================
        # CONTENT CONTAINER
        # =====================

        self.container = QFrame()

        self.container.setObjectName("option_section_container")

        self.container.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        self.container_layout = QVBoxLayout(self.container)

        self.container_layout.setContentsMargins(16, 16, 16, 16)

        self.container_layout.setSpacing(12)

        self.panel_layout.addWidget(self.container)

        # =====================
        # MAIN ASSEMBLY
        # =====================

        self.main_layout.addWidget(self.panel)

        self.set_collapsed(False)

    # =====================
    # ADD WIDGET
    # =====================

    def add_widget(self, widget):
        self.container_layout.addWidget(widget)

    # =====================
    # ADD LAYOUT
    # =====================

    def add_layout(self, layout):
        self.container_layout.addLayout(layout)

    # =====================
    # TOGGLE SECTION
    # =====================

    def toggle(self, checked=None):
        if not self.collapsible:
            return

        if checked is None:
            # Also support direct calls to toggle().
            new_state = not self.collapsed

        else:
            # Checked means expanded.
            new_state = not bool(checked)

        previous_state = self.collapsed

        self.set_collapsed(new_state)

        # Preserve the original signal behavior:
        # emit only when toggling changes the state.

        if previous_state != self.collapsed:
            self.collapsed_changed.emit(self.collapsed)

    # =====================
    # SET COLLAPSED STATE
    # =====================

    def set_collapsed(self, state):
        state = bool(state)

        self.collapsed = state

        # Content visibility

        self.container.setVisible(not state)

        self.divider.setVisible(not state)

        # Update toggle button appearance

        if self.collapsible:
            self.toggle_button.setChecked(not state)

            if state:
                self.toggle_button.setArrowType(Qt.ArrowType.RightArrow)

                self.toggle_button.setToolTip("Expand this section")

            else:
                self.toggle_button.setArrowType(Qt.ArrowType.DownArrow)

                self.toggle_button.setToolTip("Collapse this section")

        # Update card state for QSS

        self.panel.setProperty(
            "collapsed",
            state,
        )

        self.header.setProperty(
            "collapsed",
            state,
        )

        for widget in (
            self.panel,
            self.header,
        ):
            widget.style().unpolish(widget)

            widget.style().polish(widget)

            widget.update()

    # =====================
    # ENABLE / DISABLE
    # =====================

    def set_enabled(self, state):
        self.setEnabled(bool(state))

    # =====================
    # PREMIUM STYLING
    # =====================

    def apply_styles(self):
        self.setStyleSheet(
            """
            /* =========================
               MAIN COMPONENT
            ========================= */

            QWidget#option_section {
                background: transparent;
                border: none;
            }

            /* =========================
               PREMIUM SECTION CARD
            ========================= */

            QFrame#option_section_panel {
                background-color: #141e30;

                border: 1px solid #29374c;
                border-radius: 13px;
            }

            QFrame#option_section_panel:hover {
                border-color: #34465c;
            }

            QFrame#option_section_panel[
                collapsed="true"
            ] {
                background-color: #19283c;
            }

            /* =========================
               HEADER
            ========================= */

            QFrame#option_section_header {
                background-color: #1b2940;

                border: none;
                border-radius: 12px;
            }

            QFrame#option_section_header:hover {
                background-color: #203149;
            }

            QFrame#option_section_header[
                collapsed="true"
            ] {
                background-color: #19283c;
            }

            /* =========================
               EMERALD ACCENT
            ========================= */

            QFrame#option_section_accent {
                background-color: #5eead4;

                border: none;
                border-radius: 1px;
            }

            /* =========================
               COLLAPSIBLE BUTTON
            ========================= */

            QToolButton#option_section_toggle {
                background: transparent;

                color: #f1f5f9;

                border: none;
                border-radius: 8px;

                padding: 6px 9px;

                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: 700;

                text-align: left;
            }

            /* =========================
               HEADER HOVER
            ========================= */

            QToolButton#option_section_toggle:hover {
                background-color: #25384e;

                color: #f8fafc;
            }

            /* =========================
               EXPANDED STATE
            ========================= */

            QToolButton#option_section_toggle:checked {
                color: #f1f5f9;
            }

            /* =========================
               COLLAPSED STATE
            ========================= */

            QToolButton#option_section_toggle:!checked {
                color: #cbd5e1;
            }

            /* =========================
               BUTTON PRESSED
            ========================= */

            QToolButton#option_section_toggle:pressed {
                background-color: #173a40;

                color: #5eead4;
            }

            /* =========================
               KEYBOARD FOCUS
            ========================= */

            QToolButton#option_section_toggle:focus {
                border: 1px solid #5eead4;
            }

            /* =========================
               NON-COLLAPSIBLE TITLE
            ========================= */

            QLabel#option_section_title {
                background: transparent;
                border: none;

                color: #f1f5f9;

                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: 700;
            }

            /* =========================
               HEADER DIVIDER
            ========================= */

            QFrame#option_section_divider {
                background-color: #29374c;

                border: none;

                min-height: 1px;
                max-height: 1px;
            }

            /* =========================
               CONTENT CONTAINER
            ========================= */

            QFrame#option_section_container {
                background-color: transparent;

                border: none;
                border-radius: 0px;
            }

            /* =========================
               DISABLED STATES
            ========================= */

            QFrame#option_section_panel:disabled {
                background-color: #151e2d;

                border: 1px solid #253348;
            }

            QFrame#option_section_header:disabled {
                background-color: #192334;
            }

            QFrame#option_section_accent:disabled {
                background-color: #42615f;
            }

            QToolButton#option_section_toggle:disabled,
            QLabel#option_section_title:disabled {
                background: transparent;

                color: #64748b;

                border: none;
            }

            QFrame#option_section_divider:disabled {
                background-color: #253348;
            }
            """
        )
