from pathlib import Path

from PySide6.QtCore import QEvent, Qt, Signal
from PySide6.QtWidgets import (
    QBoxLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMenu,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

# =====================
# PREMIUM IMAGE TILE
# =====================


class ImageTileButton(QPushButton):
    def __init__(self, image_path, index, parent=None):
        super().__init__(parent)

        self.image_path = Path(image_path)
        self.image_index = index

        self.setObjectName("image_list_tile")
        self.setProperty("selected", False)

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.setFixedHeight(86)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.setToolTip(str(self.image_path))

        self.setAccessibleName(f"Select image: {self.image_path.name}")

        self.setup_ui()

    # =====================
    # TILE CONTENT
    # =====================

    def setup_ui(self):
        layout = QHBoxLayout(self)

        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(10)

        # File icon

        self.icon_label = QLabel("▧")
        self.icon_label.setObjectName("image_tile_icon")

        self.icon_label.setFixedSize(36, 40)

        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # File information

        information_layout = QVBoxLayout()
        information_layout.setSpacing(5)

        self.filename_label = QLabel(self.image_path.name)

        self.filename_label.setObjectName("image_tile_name")

        self.filename_label.setWordWrap(False)

        self.filename_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        extension = self.image_path.suffix.lstrip(".").upper() or "IMAGE"

        self.metadata_label = QLabel(f"{extension}  •  {index_text(self.image_index)}")

        self.metadata_label.setObjectName("image_tile_metadata")

        information_layout.addWidget(self.filename_label)

        information_layout.addWidget(self.metadata_label)

        information_layout.addStretch()

        layout.addWidget(self.icon_label)
        layout.addLayout(information_layout, 1)

        # Child labels must not intercept clicks.

        for label in (
            self.icon_label,
            self.filename_label,
            self.metadata_label,
        ):
            label.setAttribute(
                Qt.WidgetAttribute.WA_TransparentForMouseEvents,
                True,
            )

    # =====================
    # TRUNCATE LONG FILENAMES
    # =====================

    def resizeEvent(self, event):
        super().resizeEvent(event)

        available_width = max(
            45,
            self.width() - 82,
        )

        metrics = self.filename_label.fontMetrics()

        display_name = metrics.elidedText(
            self.image_path.name,
            Qt.TextElideMode.ElideMiddle,
            available_width,
        )

        self.filename_label.setText(display_name)


def index_text(index):
    return f"FILE {index + 1:02d}"


# =====================
# IMAGE LIST WIDGET
# =====================


class ImageListWidget(QWidget):
    image_selected = Signal(Path)
    images_changed = Signal(list)

    MAX_COLUMNS = 6
    MIN_TILE_WIDTH = 148
    GRID_SPACING = 10

    def __init__(self):
        super().__init__()

        self.images = []
        self.buttons = []

        self.selected_index = None
        self.selected_image = None

        self._column_count = 0

        self.setObjectName("image_list_widget")

        self.setup_ui()
        self.apply_styles()

        self.refresh()

    # =====================
    # MAIN USER INTERFACE
    # =====================

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.setSpacing(0)

        # =====================
        # MAIN CARD
        # =====================

        self.card = QFrame()

        self.card.setObjectName("image_list_card")

        card_layout = QVBoxLayout(self.card)

        card_layout.setContentsMargins(20, 20, 20, 18)

        card_layout.setSpacing(14)

        # =====================
        # HEADER
        # =====================

        header = QHBoxLayout()
        header.setSpacing(12)

        header_text = QVBoxLayout()
        header_text.setSpacing(6)

        eyebrow = QLabel("IMAGE WORKSPACE")

        eyebrow.setObjectName("image_list_eyebrow")

        title = QLabel("Image Collection")

        title.setObjectName("image_list_title")

        description = QLabel("Manage images added to your processing queue.")

        description.setObjectName("image_list_description")

        description.setWordWrap(True)

        header_text.addWidget(eyebrow)
        header_text.addWidget(title)
        header_text.addWidget(description)

        # Image count

        self.count_label = QLabel("0 IMAGES")

        self.count_label.setObjectName("image_list_count")

        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header.addLayout(
            header_text,
            1,
        )

        header.addWidget(
            self.count_label,
            0,
            Qt.AlignmentFlag.AlignTop,
        )

        card_layout.addLayout(header)

        # =====================
        # IMAGE GRID SCROLL AREA
        # =====================

        self.scroll = QScrollArea()

        self.scroll.setObjectName("image_list_scroll")

        self.scroll.setWidgetResizable(True)

        self.scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.scroll.setFixedHeight(236)

        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Grid container

        self.container = QWidget()

        self.container.setObjectName("image_list_container")

        self.grid = QGridLayout(self.container)

        self.grid.setContentsMargins(6, 6, 6, 6)

        self.grid.setHorizontalSpacing(self.GRID_SPACING)

        self.grid.setVerticalSpacing(self.GRID_SPACING)

        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll.setWidget(self.container)

        self.scroll.viewport().installEventFilter(self)

        card_layout.addWidget(self.scroll)

        # =====================
        # SELECTION STATUS
        # =====================

        selection_layout = QHBoxLayout()
        selection_layout.setSpacing(8)

        selection_icon = QLabel("●")

        selection_icon.setObjectName("image_list_selection_icon")

        self.selection_label = QLabel("Select an image to inspect or remove it.")

        self.selection_label.setObjectName("image_list_selection_text")

        self.selection_label.setWordWrap(True)

        selection_layout.addWidget(selection_icon)

        selection_layout.addWidget(
            self.selection_label,
            1,
        )

        card_layout.addLayout(selection_layout)

        # =====================
        # BUTTON BAR
        # =====================

        self.button_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)

        self.button_layout.setSpacing(10)

        # Sort

        self.sort_button = QPushButton("↕  Sort Images")

        self.sort_button.setObjectName("image_list_sort_button")

        self.sort_button.setMinimumHeight(40)

        self.sort_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.sort_button.clicked.connect(self.show_sort_menu)

        # Remove selected

        self.remove_button = QPushButton("✕  Remove Selected")

        self.remove_button.setObjectName("image_list_remove_button")

        self.remove_button.setMinimumHeight(40)

        self.remove_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.remove_button.clicked.connect(self.remove_selected)

        # Clear all

        self.delete_all_button = QPushButton("Clear List")

        self.delete_all_button.setObjectName("image_list_clear_button")

        self.delete_all_button.setMinimumHeight(40)

        self.delete_all_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.delete_all_button.clicked.connect(self.delete_all)

        self.button_layout.addWidget(
            self.sort_button,
            1,
        )

        self.button_layout.addWidget(
            self.remove_button,
            1,
        )

        self.button_layout.addWidget(
            self.delete_all_button,
            1,
        )

        card_layout.addLayout(self.button_layout)

        main_layout.addWidget(self.card)

    # =====================
    # EMPTY STATE
    # =====================

    def create_empty_state(self):
        frame = QFrame()

        frame.setObjectName("image_list_empty_state")

        frame.setMinimumHeight(175)

        layout = QVBoxLayout(frame)

        layout.setContentsMargins(18, 20, 18, 20)

        layout.setSpacing(9)

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = QLabel("▧")

        icon.setObjectName("image_list_empty_icon")

        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("No Images Added")

        title.setObjectName("image_list_empty_title")

        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Import images using the drop area to see them here.")

        subtitle.setObjectName("image_list_empty_description")

        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle.setWordWrap(True)

        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        return frame

    # =====================
    # SET IMAGE COLLECTION
    # =====================

    def set_images(self, images):
        self.images = [Path(image) for image in images]

        self.selected_index = None
        self.selected_image = None

        self.refresh()

    # =====================
    # REFRESH IMAGE GRID
    # =====================

    def refresh(self):
        previous_selection = self.selected_image

        self.clear_grid()

        self.selected_index = None
        self.selected_image = None

        self.update_count()

        # =====================
        # EMPTY COLLECTION
        # =====================

        if not self.images:
            empty_state = self.create_empty_state()

            self.grid.addWidget(
                empty_state,
                0,
                0,
                1,
                self.MAX_COLUMNS,
            )

            self._column_count = 0

            self.update_action_states()

            self.images_changed.emit(self.images.copy())

            return

        # =====================
        # CREATE IMAGE TILES
        # =====================

        for index, image in enumerate(self.images):
            button = ImageTileButton(
                image,
                index,
                self.container,
            )

            button.clicked.connect(lambda checked=False, i=index: self.select_image(i))

            self.buttons.append(button)

        # Apply responsive layout

        self._column_count = 0
        self.reflow_grid()

        # =====================
        # RESTORE SELECTION
        # =====================

        if previous_selection is not None and previous_selection in self.images:
            index = self.images.index(previous_selection)

            self.select_image(
                index,
                emit_signal=False,
            )

        self.update_action_states()

        self.images_changed.emit(self.images.copy())

    # =====================
    # IMAGE SELECTION
    # =====================

    def select_image(
        self,
        index,
        emit_signal=True,
    ):
        if not (0 <= index < len(self.images)):
            return

        # Clear previous selection

        if self.selected_index is not None:
            if self.selected_index < len(self.buttons):
                previous_button = self.buttons[self.selected_index]

                self.set_tile_selected(
                    previous_button,
                    False,
                )

        # Apply new selection

        self.selected_index = index

        self.selected_image = self.images[index]

        button = self.buttons[index]

        self.set_tile_selected(
            button,
            True,
        )

        self.update_action_states()

        # Notify image preview / info panel

        if emit_signal:
            self.image_selected.emit(self.selected_image)

    # =====================
    # TILE SELECTED STATE
    # =====================

    def set_tile_selected(
        self,
        button,
        selected,
    ):
        button.setProperty(
            "selected",
            bool(selected),
        )

        button.style().unpolish(button)

        button.style().polish(button)

        button.update()

    # =====================
    # UPDATE IMAGE COUNT
    # =====================

    def update_count(self):
        count = len(self.images)

        if count == 1:
            self.count_label.setText("1 IMAGE")
        else:
            self.count_label.setText(f"{count} IMAGES")

    # =====================
    # UPDATE BUTTON STATES
    # =====================

    def update_action_states(self):
        has_images = bool(self.images)

        has_selection = self.selected_index is not None

        self.sort_button.setEnabled(len(self.images) > 1)

        self.remove_button.setEnabled(has_selection)

        self.delete_all_button.setEnabled(has_images)

        if has_selection and self.selected_image is not None:
            filename = self.selected_image.name

            self.selection_label.setText(f"Selected: {filename}")

            self.selection_label.setToolTip(str(self.selected_image))

        elif has_images:
            self.selection_label.setText("Select an image to inspect or remove it.")

            self.selection_label.setToolTip("")

        else:
            self.selection_label.setText("Your image collection is empty.")

            self.selection_label.setToolTip("")

    # =====================
    # CLEAR GRID WIDGETS
    # =====================

    def clear_grid(self):
        while self.grid.count():
            item = self.grid.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.hide()
                widget.deleteLater()

        self.buttons.clear()

        self._column_count = 0

    # =====================
    # RESPONSIVE GRID
    # =====================

    def calculate_columns(self):
        viewport_width = self.scroll.viewport().width()

        available_width = max(
            1,
            viewport_width - 12,
        )

        item_width = self.MIN_TILE_WIDTH + self.GRID_SPACING

        columns = (available_width + self.GRID_SPACING) // item_width

        return max(
            1,
            min(
                self.MAX_COLUMNS,
                columns,
            ),
        )

    def reflow_grid(self):
        if not self.buttons:
            return

        columns = self.calculate_columns()

        if columns == self._column_count:
            return

        # Remove existing positions without
        # deleting the actual buttons.

        for button in self.buttons:
            self.grid.removeWidget(button)

        # Reset previous column stretch

        for column in range(self.MAX_COLUMNS):
            self.grid.setColumnStretch(
                column,
                1 if column < columns else 0,
            )

        # Reposition tiles

        for index, button in enumerate(self.buttons):
            row = index // columns
            column = index % columns

            self.grid.addWidget(
                button,
                row,
                column,
            )

        self._column_count = columns

    # =====================
    # VIEWPORT RESIZE
    # =====================

    def eventFilter(
        self,
        watched,
        event,
    ):
        if watched is self.scroll.viewport() and event.type() == QEvent.Type.Resize:
            self.reflow_grid()

        return super().eventFilter(
            watched,
            event,
        )

    # =====================
    # RESPONSIVE ACTION BAR
    # =====================

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if not hasattr(
            self,
            "button_layout",
        ):
            return

        if self.width() < 470:
            self.button_layout.setDirection(QBoxLayout.Direction.TopToBottom)
        else:
            self.button_layout.setDirection(QBoxLayout.Direction.LeftToRight)

    # =====================
    # SORT MENU
    # =====================

    def show_sort_menu(self):
        if len(self.images) < 2:
            return

        menu = QMenu(self)

        menu.setObjectName("image_list_sort_menu")

        asc_action = menu.addAction("↑  Name: A to Z")

        desc_action = menu.addAction("↓  Name: Z to A")

        action = menu.exec(
            self.sort_button.mapToGlobal(self.sort_button.rect().bottomLeft())
        )

        if action == asc_action:
            self.sort_ascending_names()

        elif action == desc_action:
            self.sort_descending_names()

    # =====================
    # REMOVE SELECTED
    # =====================

    def remove_selected(self):
        if self.selected_index is None:
            return

        if not (0 <= self.selected_index < len(self.images)):
            return

        del self.images[self.selected_index]

        self.selected_index = None
        self.selected_image = None

        self.refresh()

    # =====================
    # CLEAR IMAGE LIST
    # =====================

    def delete_all(self):
        if not self.images:
            return

        self.images.clear()

        self.selected_index = None
        self.selected_image = None

        self.refresh()

    # =====================
    # SORT ASCENDING
    # =====================

    def sort_ascending_names(self):
        self.images.sort(
            key=lambda path: (
                path.name.casefold(),
                str(path).casefold(),
            )
        )

        self.refresh()

    # =====================
    # SORT DESCENDING
    # =====================

    def sort_descending_names(self):
        self.images.sort(
            key=lambda path: (
                path.name.casefold(),
                str(path).casefold(),
            ),
            reverse=True,
        )

        self.refresh()

    # =====================
    # GET IMAGES
    # =====================

    def get_images(self):
        return self.images.copy()

    # =====================
    # PREMIUM STYLING
    # =====================

    def apply_styles(self):
        self.setStyleSheet(
            """
            /* MAIN WIDGET */

            QWidget#image_list_widget {
                background: transparent;
                border: none;
            }

            /* MAIN CARD */

            QFrame#image_list_card {
                background-color: #141e30;
                border: 1px solid #29374c;
                border-radius: 16px;
            }

            /* HEADER */

            QLabel#image_list_eyebrow {
                color: #5eead4;
                background: transparent;
                border: none;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#image_list_title {
                color: #f1f5f9;
                background: transparent;
                border: none;
                font-family: "Segoe UI";
                font-size: 19px;
                font-weight: 700;
            }

            QLabel#image_list_description {
                color: #94a3b8;
                background: transparent;
                border: none;
                font-family: "Segoe UI";
                font-size: 12px;
            }

            /* IMAGE COUNT */

            QLabel#image_list_count {
                background-color: #173a40;
                color: #5eead4;
                border: 1px solid #28665f;
                border-radius: 8px;
                padding: 8px 12px;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
            }

            /* SCROLL AREA */

            QScrollArea#image_list_scroll {
                background: transparent;
                border: none;
            }

            QWidget#image_list_container {
                background: transparent;
                border: none;
            }

            /* IMAGE TILES */

            QPushButton#image_list_tile {
                background-color: #1b2940;
                color: #d5deea;
                border: 1px solid #304259;
                border-radius: 11px;
                text-align: left;
            }

            QPushButton#image_list_tile:hover {
                background-color: #21334a;
                border: 1px solid #426273;
            }

            QPushButton#image_list_tile:pressed {
                background-color: #203e46;
            }

            QPushButton#image_list_tile[selected="true"] {
                background-color: #173a40;
                border: 2px solid #5eead4;
            }

            QPushButton#image_list_tile[selected="true"]:hover {
                background-color: #1c4649;
                border: 2px solid #99f6e4;
            }

            QPushButton#image_list_tile:focus {
                border: 2px solid #5eead4;
            }

            /* TILE ICON */

            QLabel#image_tile_icon {
                background-color: #173a40;
                color: #5eead4;
                border: 1px solid #285d60;
                border-radius: 9px;
                font-family: "Segoe UI Symbol";
                font-size: 23px;
                font-weight: 700;
            }

            /* TILE FILENAME */

            QLabel#image_tile_name {
                color: #f1f5f9;
                background: transparent;
                border: none;
                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 600;
            }

            /* TILE METADATA */

            QLabel#image_tile_metadata {
                color: #94a3b8;
                background: transparent;
                border: none;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 500;
            }

            /* EMPTY STATE */

            QFrame#image_list_empty_state {
                background-color: #111b2b;
                border: 1px dashed #36546b;
                border-radius: 12px;
            }

            QLabel#image_list_empty_icon {
                color: #5eead4;
                background: transparent;
                border: none;
                font-family: "Segoe UI Symbol";
                font-size: 33px;
            }

            QLabel#image_list_empty_title {
                color: #f1f5f9;
                background: transparent;
                border: none;
                font-family: "Segoe UI";
                font-size: 14px;
                font-weight: 700;
            }

            QLabel#image_list_empty_description {
                color: #64748b;
                background: transparent;
                border: none;
                font-family: "Segoe UI";
                font-size: 11px;
            }

            /* SELECTION STATUS */

            QLabel#image_list_selection_icon {
                color: #5eead4;
                background: transparent;
                border: none;
                font-size: 9px;
            }

            QLabel#image_list_selection_text {
                color: #94a3b8;
                background: transparent;
                border: none;
                font-family: "Segoe UI";
                font-size: 11px;
            }

            /* SORT BUTTON */

            QPushButton#image_list_sort_button {
                background-color: #1b2940;
                color: #d5deea;
                border: 1px solid #38536b;
                border-radius: 9px;
                padding: 8px 12px;
                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton#image_list_sort_button:hover {
                background-color: #24384e;
                color: #f8fafc;
                border-color: #5eead4;
            }

            /* REMOVE BUTTON */

            QPushButton#image_list_remove_button {
                background-color: #173a40;
                color: #5eead4;
                border: 1px solid #28665f;
                border-radius: 9px;
                padding: 8px 12px;
                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 700;
            }

            QPushButton#image_list_remove_button:hover {
                background-color: #1c4649;
                color: #99f6e4;
                border-color: #5eead4;
            }

            /* CLEAR BUTTON */

            QPushButton#image_list_clear_button {
                background-color: #35232f;
                color: #fca5a5;
                border: 1px solid #75404c;
                border-radius: 9px;
                padding: 8px 12px;
                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 700;
            }

            QPushButton#image_list_clear_button:hover {
                background-color: #512c38;
                color: #fecaca;
            }

            /* BUTTON PRESSED */

            QPushButton#image_list_sort_button:pressed,
            QPushButton#image_list_remove_button:pressed {
                background-color: #285d60;
            }

            QPushButton#image_list_clear_button:pressed {
                background-color: #663440;
            }

            /* DISABLED BUTTONS */

            QPushButton#image_list_sort_button:disabled,
            QPushButton#image_list_remove_button:disabled,
            QPushButton#image_list_clear_button:disabled {
                background-color: #202b3b;
                color: #64748b;
                border: 1px solid #354459;
            }

            /* SORT POPUP */

            QMenu#image_list_sort_menu {
                background-color: #141e30;
                color: #d5deea;
                border: 1px solid #304259;
                border-radius: 9px;
                padding: 6px;
                font-family: "Segoe UI";
                font-size: 12px;
            }

            QMenu#image_list_sort_menu::item {
                padding: 9px 22px;
                border-radius: 6px;
            }

            QMenu#image_list_sort_menu::item:selected {
                background-color: #173a40;
                color: #5eead4;
            }

            /* VERTICAL SCROLLBAR */

            QScrollBar:vertical {
                background-color: #141e30;
                width: 7px;
                margin: 0;
                border: none;
            }

            QScrollBar::handle:vertical {
                background-color: #334155;
                border-radius: 3px;
                min-height: 28px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #5eead4;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
                border: none;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }
            """
        )
