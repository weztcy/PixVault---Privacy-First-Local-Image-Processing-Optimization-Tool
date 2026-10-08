"""Reusable processing toggle card, styled using the global PixVault roles."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget

from ui.components.processing_options.common.checkbox_field import CheckboxField
from ui.components.processing_options.common.warning_label import WarningLabel
from ui.styles.pixvault_theme import apply_page_theme, role


class ProcessingCard(QWidget):
    enabled_changed = Signal(bool)
    settings_changed = Signal(dict)

    def __init__(self, title, option_widget, parent=None):
        super().__init__(parent)
        self.title = str(title)
        self.option_widget = option_widget
        self.setup_ui()
        apply_page_theme(self)

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.frame = role(QFrame(self), "card")
        self.frame.setObjectName("processing_card")
        self.card_layout = QVBoxLayout(self.frame)
        self.card_layout.setContentsMargins(18, 18, 18, 18)
        self.card_layout.setSpacing(12)

        self.enable_field = CheckboxField(self.title, False)
        self.enable_checkbox = self.enable_field.checkbox  # existing consumer API
        self.card_layout.addWidget(self.enable_field)

        self.warning = WarningLabel(self)
        self.card_layout.addWidget(self.warning)

        self.content = QWidget(self.frame)
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(9)
        self.content_layout.addWidget(self.option_widget)
        self.card_layout.addWidget(self.content)
        self.main_layout.addWidget(self.frame)
        self.content.hide()
        self.option_widget.setEnabled(False)

        self.enable_field.value_changed.connect(self.toggle_enabled)
        if hasattr(self.option_widget, "settings_changed"):
            self.option_widget.settings_changed.connect(self.emit_settings)

    def toggle_enabled(self, state):
        enabled = bool(state)
        self.content.setVisible(enabled)
        self.option_widget.setEnabled(enabled)
        self.enabled_changed.emit(enabled)
        self.emit_settings()

    def set_enabled(self, enabled):
        self.enable_checkbox.setChecked(bool(enabled))

    def is_enabled(self):
        return self.enable_checkbox.isChecked()

    def get_settings(self):
        if not self.is_enabled():
            return {}
        settings = dict(self.option_widget.get_settings())
        settings["enabled"] = True
        return settings

    def set_warning(self, message):
        self.warning.show_warning(message)

    def clear_warning(self):
        self.warning.clear_warning()

    def reset(self):
        self.set_enabled(False)
        self.option_widget.reset()
        self.clear_warning()

    def emit_settings(self, *_args):
        self.settings_changed.emit(self.get_settings())
