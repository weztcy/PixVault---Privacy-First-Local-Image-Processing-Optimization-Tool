from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QLabel, QToolButton, QVBoxLayout, QWidget


class OptionSection(QWidget):
    collapsed_changed = Signal(bool)

    def __init__(self, title, collapsible=True, parent=None):

        super().__init__(parent)

        self.title = title

        self.collapsible = collapsible

        self.collapsed = False

        self.setup_ui()

    def setup_ui(self):

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setSpacing(5)

        header = QWidget()

        header_layout = QVBoxLayout(header)

        header_layout.setContentsMargins(0, 0, 0, 0)

        if self.collapsible:
            self.toggle_button = QToolButton()

            self.toggle_button.setText(self.title)

            self.toggle_button.setCheckable(True)

            self.toggle_button.setChecked(True)

            self.toggle_button.clicked.connect(self.toggle)

            header_layout.addWidget(self.toggle_button)

        else:
            label = QLabel(self.title)

            label.setObjectName("section_title")

            header_layout.addWidget(label)

        self.main_layout.addWidget(header)

        self.container = QFrame()

        self.container_layout = QVBoxLayout(self.container)

        self.container_layout.setSpacing(8)

        self.main_layout.addWidget(self.container)

    def add_widget(self, widget):

        self.container_layout.addWidget(widget)

    def add_layout(self, layout):

        self.container_layout.addLayout(layout)

    def toggle(self):

        self.collapsed = not self.toggle_button.isChecked()

        self.container.setVisible(not self.collapsed)

        self.collapsed_changed.emit(self.collapsed)

    def set_collapsed(self, state):

        self.collapsed = state

        self.container.setVisible(not state)

        if self.collapsible:
            self.toggle_button.setChecked(not state)

    def set_enabled(self, state):

        self.setEnabled(state)
