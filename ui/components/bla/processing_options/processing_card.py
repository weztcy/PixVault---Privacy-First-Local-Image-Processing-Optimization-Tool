from PySide6.QtCore import Signal
from PySide6.QtWidgets import QCheckBox, QFrame, QVBoxLayout, QWidget

from ui.components.processing_options.common.warning_label import WarningLabel


class ProcessingCard(QWidget):
    enabled_changed = Signal(bool)

    settings_changed = Signal(dict)

    def __init__(self, title, option_widget, parent=None):

        super().__init__(parent)

        self.title = title

        self.option_widget = option_widget

        self.setup_ui()

    def setup_ui(self):

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setSpacing(8)

        self.frame = QFrame()

        self.frame.setObjectName("processing_card")

        self.card_layout = QVBoxLayout(self.frame)

        self.card_layout.setSpacing(8)

        # =====================
        # ENABLE CHECKBOX
        # =====================

        self.enable_checkbox = QCheckBox(self.title)

        self.enable_checkbox.setChecked(False)

        self.enable_checkbox.stateChanged.connect(self.toggle_enabled)

        self.card_layout.addWidget(self.enable_checkbox)

        # =====================
        # WARNING
        # =====================

        self.warning = WarningLabel()

        self.card_layout.addWidget(self.warning)

        # =====================
        # CONTENT
        # =====================

        self.content = QFrame()

        self.content_layout = QVBoxLayout(self.content)

        self.content_layout.setContentsMargins(10, 5, 10, 5)

        self.content_layout.addWidget(self.option_widget)

        self.card_layout.addWidget(self.content)

        self.main_layout.addWidget(self.frame)

        self.content.setVisible(False)

    def toggle_enabled(self, state):

        enabled = state != 0

        self.content.setVisible(enabled)

        self.option_widget.setEnabled(enabled)

        self.enabled_changed.emit(enabled)

        self.emit_settings()

    def set_enabled(self, enabled):

        self.enable_checkbox.setChecked(enabled)

    def is_enabled(self):

        return self.enable_checkbox.isChecked()

    def get_settings(self):

        if not self.is_enabled():
            return {}

        settings = self.option_widget.get_settings()

        settings["enabled"] = True

        return settings

    def set_warning(self, message):

        self.warning.show_warning(message)

    def clear_warning(self):

        self.warning.clear_warning()

    def reset(self):

        self.enable_checkbox.setChecked(False)

        self.option_widget.reset()

        self.clear_warning()

    def emit_settings(self):

        self.settings_changed.emit(self.get_settings())
