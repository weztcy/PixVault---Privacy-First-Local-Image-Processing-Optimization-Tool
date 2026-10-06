from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QMenu,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class ImageListWidget(QWidget):
    image_selected = Signal(Path)

    images_changed = Signal(list)

    def __init__(self):

        super().__init__()

        self.images = []

        self.buttons = []

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setSpacing(8)

        # =====================
        # IMAGE GRID
        # =====================

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(True)

        self.scroll.setFixedHeight(150)

        self.container = QWidget()

        self.grid = QGridLayout(self.container)

        self.grid.setSpacing(5)

        self.grid.setContentsMargins(5, 5, 5, 5)

        self.scroll.setWidget(self.container)

        # =====================
        # BUTTON BAR
        # =====================

        button_layout = QHBoxLayout()

        self.sort_button = QPushButton("↕ Sort Name")

        self.remove_button = QPushButton("✖ Remove Selected")

        self.delete_all_button = QPushButton("🗑 Delete All")

        self.sort_button.clicked.connect(self.show_sort_menu)

        self.remove_button.clicked.connect(self.remove_selected)

        self.delete_all_button.clicked.connect(self.delete_all)

        button_layout.addWidget(self.sort_button)

        button_layout.addWidget(self.remove_button)

        button_layout.addWidget(self.delete_all_button)

        layout.addWidget(self.scroll)

        layout.addLayout(button_layout)

    def set_images(self, images):

        self.images = [Path(image) for image in images]

        self.refresh()

    def refresh(self):

        self.clear_grid()

        for index, image in enumerate(self.images):
            button = QPushButton(image.name)

            button.setToolTip(str(image))

            button.setMinimumHeight(30)

            # rata kiri

            button.setStyleSheet(
                """
                QPushButton {
                    text-align: left;
                    padding-left: 8px;
                }
                """
            )

            button.clicked.connect(
                lambda checked=False, path=image: self.image_selected.emit(path)
            )

            row = index // 6

            column = index % 6

            self.grid.addWidget(button, row, column)

            self.buttons.append(button)

        # fixed 6 columns

        for column in range(6):
            self.grid.setColumnStretch(column, 1)

        self.images_changed.emit(self.images.copy())

    def clear_grid(self):

        while self.grid.count():
            item = self.grid.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        self.buttons.clear()

    def show_sort_menu(self):

        menu = QMenu(self)

        asc_action = menu.addAction("↑ Sort Ascending")

        desc_action = menu.addAction("↓ Sort Descending")

        action = menu.exec(
            self.sort_button.mapToGlobal(self.sort_button.rect().bottomLeft())
        )

        if action == asc_action:
            self.sort_ascending_names()

        elif action == desc_action:
            self.sort_descending_names()

    def remove_selected(self):

        selected = self.focusWidget()

        if selected not in self.buttons:
            return

        index = self.buttons.index(selected)

        del self.images[index]

        self.refresh()

    def delete_all(self):

        self.images.clear()

        self.refresh()

    def sort_ascending_names(self):

        self.images.sort(key=lambda x: x.name.lower())

        self.refresh()

    def sort_descending_names(self):

        self.images.sort(key=lambda x: x.name.lower(), reverse=True)

        self.refresh()

    def get_images(self):

        return self.images.copy()
