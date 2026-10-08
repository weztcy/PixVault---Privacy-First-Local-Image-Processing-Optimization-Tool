from PySide6.QtCore import (
    QPointF,
    Qt,
    Signal,
)
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListView,
    QVBoxLayout,
    QWidget,
)

# =====================
# PREMIUM COMBO BOX
# =====================


class PremiumComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("premium_dropdown")

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.setMinimumHeight(44)

        self.setMaxVisibleItems(10)

        # Custom dropdown list

        view = QListView(self)

        view.setObjectName("premium_dropdown_view")

        view.setFrameShape(QListView.Shape.NoFrame)

        view.setSpacing(2)

        view.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        self.setView(view)

        self.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon
        )

        self.setMinimumContentsLength(12)

    # =====================
    # CUSTOM ARROW
    # =====================

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if not self.isEnabled():
            arrow_color = QColor("#64748b")

        elif self.hasFocus() or self.underMouse():
            arrow_color = QColor("#5eead4")

        else:
            arrow_color = QColor("#94a3b8")

        pen = QPen(arrow_color)
        pen.setWidthF(1.8)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)

        painter.setPen(pen)

        center_x = self.width() - 19
        center_y = self.height() / 2

        painter.drawLine(
            QPointF(center_x - 5, center_y - 2),
            QPointF(center_x, center_y + 3),
        )

        painter.drawLine(
            QPointF(center_x, center_y + 3),
            QPointF(center_x + 5, center_y - 2),
        )

        painter.end()


# =====================
# DROPDOWN FIELD
# =====================


class DropdownField(QWidget):
    value_changed = Signal(str)

    def __init__(
        self,
        title,
        items,
        default=None,
    ):
        super().__init__()

        self.setObjectName("dropdown_field")

        self.setup_ui(
            title,
            items,
            default,
        )

        self.apply_styles()

    # =====================
    # USER INTERFACE
    # =====================

    def setup_ui(
        self,
        title,
        items,
        default,
    ):
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.setSpacing(9)

        # =====================
        # FIELD LABEL
        # =====================

        header_layout = QHBoxLayout()

        header_layout.setContentsMargins(2, 0, 2, 0)

        header_layout.setSpacing(8)

        self.label = QLabel(title)

        self.label.setObjectName("dropdown_field_label")

        self.label.setWordWrap(True)

        header_layout.addWidget(self.label)

        header_layout.addStretch()

        # =====================
        # COMBO BOX
        # =====================

        self.combo = PremiumComboBox()

        self.combo.setAccessibleName(str(title))

        self.combo.addItems(items)

        if default is not None:
            self.combo.setCurrentText(str(default))

        # =====================
        # ASSEMBLE LAYOUT
        # =====================

        main_layout.addLayout(header_layout)

        main_layout.addWidget(self.combo)

        # =====================
        # SIGNAL CONNECTION
        # =====================

        self.combo.currentTextChanged.connect(self.value_changed.emit)

    # =====================
    # GET VALUE
    # =====================

    def value(self):
        return self.combo.currentText()

    # =====================
    # SET VALUE
    # =====================

    def set_value(self, value):
        self.combo.setCurrentText(str(value))

    # =====================
    # PREMIUM STYLING
    # =====================

    def apply_styles(self):
        self.setStyleSheet(
            """
            /* =========================
               FIELD CONTAINER
            ========================= */

            QWidget#dropdown_field {
                background-color: transparent;
                border: none;
            }

            /* =========================
               FIELD LABEL
            ========================= */

            QLabel#dropdown_field_label {
                color: #cbd5e1;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 600;

                background: transparent;
                border: none;
            }

            /* =========================
               COMBO BOX
            ========================= */

            QComboBox#premium_dropdown {
                background-color: #1b2940;

                color: #f1f5f9;

                border: 1px solid #304259;
                border-radius: 10px;

                padding: 8px 44px 8px 14px;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 500;

                selection-background-color: #173a40;
                selection-color: #5eead4;
            }

            /* =========================
               HOVER
            ========================= */

            QComboBox#premium_dropdown:hover {
                background-color: #203149;

                border: 1px solid #426273;
            }

            /* =========================
               FOCUS
            ========================= */

            QComboBox#premium_dropdown:focus {
                background-color: #1c2e43;

                border: 1px solid #5eead4;
            }

            /* =========================
               DROP-DOWN AREA
            ========================= */

            QComboBox#premium_dropdown::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;

                width: 36px;

                background-color: transparent;

                border: none;
                border-left: 1px solid #304259;

                border-top-right-radius: 9px;
                border-bottom-right-radius: 9px;
            }

            QComboBox#premium_dropdown::down-arrow {
                image: none;

                width: 0px;
                height: 0px;
            }

            /* =========================
               DISABLED STATE
            ========================= */

            QComboBox#premium_dropdown:disabled {
                background-color: #151e2d;

                color: #64748b;

                border: 1px solid #253348;
            }

            /* =========================
               DROPDOWN LIST
            ========================= */

            QListView#premium_dropdown_view {
                background-color: #141e30;

                color: #d5deea;

                border: 1px solid #304259;

                outline: none;

                font-family: "Segoe UI";
                font-size: 12px;

                padding: 5px;
            }

            QListView#premium_dropdown_view::item {
                background-color: transparent;

                color: #d5deea;

                border: none;
                border-radius: 6px;

                padding: 9px 12px;

                min-height: 18px;
            }

            QListView#premium_dropdown_view::item:hover {
                background-color: #203149;

                color: #f8fafc;
            }

            QListView#premium_dropdown_view::item:selected {
                background-color: #173a40;

                color: #5eead4;
            }

            QListView#premium_dropdown_view::item:disabled {
                color: #64748b;
                background-color: transparent;
            }

            /* =========================
               POPUP SCROLLBAR
            ========================= */

            QListView#premium_dropdown_view QScrollBar:vertical {
                background-color: #141e30;

                width: 7px;
                margin: 0;

                border: none;
            }

            QListView#premium_dropdown_view QScrollBar::handle:vertical {
                background-color: #334155;

                border-radius: 3px;

                min-height: 25px;
            }

            QListView#premium_dropdown_view QScrollBar::handle:vertical:hover {
                background-color: #5eead4;
            }

            QListView#premium_dropdown_view QScrollBar::add-line:vertical,
            QListView#premium_dropdown_view QScrollBar::sub-line:vertical {
                height: 0;
                border: none;
            }

            QListView#premium_dropdown_view QScrollBar::add-page:vertical,
            QListView#premium_dropdown_view QScrollBar::sub-page:vertical {
                background: transparent;
            }
            """
        )
