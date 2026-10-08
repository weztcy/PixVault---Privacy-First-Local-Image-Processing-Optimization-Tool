"""Processing options composition without a nested scroll area.

Parent pages already own the page scrollbar (as in ConvertPage).  The panel
assembles independent cards and exposes the original get_settings() API.
"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget

from ui.components.processing_options.bitdepth_options import BitDepthOptions
from ui.components.processing_options.colorspace_options import ColorSpaceOptions
from ui.components.processing_options.compression_options import CompressionOptions
from ui.components.processing_options.crop_options import CropOptions
from ui.components.processing_options.dpi_options import DPIOptions
from ui.components.processing_options.metadata_options import MetadataOptions
from ui.components.processing_options.processing_card import ProcessingCard
from ui.components.processing_options.resize_options import ResizeOptions
from ui.components.processing_options.transform_options import TransformOptions


class ProcessingOptionsPanel(QWidget):
    settings_changed = Signal(dict)
    PROCESSORS = {
        "resize": ("Resize", ResizeOptions),
        "crop": ("Crop", CropOptions),
        "transform": ("Transform", TransformOptions),
        "compression": ("Compression", CompressionOptions),
        "dpi": ("DPI / Resolution", DPIOptions),
        "colorspace": ("Color Space", ColorSpaceOptions),
        "bitdepth": ("Bit Depth", BitDepthOptions),
        "metadata": ("Metadata", MetadataOptions),
    }

    def __init__(self):
        super().__init__()
        self.current_format = None
        self.cards = {}
        self._updating = True
        self.setup_ui()
        self._updating = False

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(14)
        self.container = self  # compatibility: root is now the container
        self.scroll = None  # parent page controls vertical scrolling
        self.create_cards()

    def create_cards(self):
        for key, (title, widget_class) in self.PROCESSORS.items():
            card = ProcessingCard(title, widget_class(), self)
            self.cards[key] = card
            self.layout.addWidget(card)
            card.settings_changed.connect(self.emit_settings)
        self.layout.addStretch(0)

    def set_format(self, format_name):
        self._updating = True
        try:
            self.current_format = str(format_name or "").upper()
            for card in self.cards.values():
                card.option_widget.set_format(self.current_format)
        finally:
            self._updating = False
        self.emit_settings()

    def get_operations(self):
        return [
            settings
            for card in self.cards.values()
            if (settings := card.get_settings())
        ]

    def validate_dependencies(self):
        warnings = []
        colorspace_card = self.cards["colorspace"]
        metadata_card = self.cards["metadata"]
        dpi_card = self.cards["dpi"]
        colorspace = colorspace_card.get_settings()
        metadata = metadata_card.get_settings()
        has_dpi = dpi_card.is_enabled()
        target = str(colorspace.get("target", "sRGB")).lower()
        removing_all = metadata.get("mode") == "all"
        removing_icc = removing_all or "icc_profile" in metadata.get("remove", [])

        if (
            colorspace
            and metadata
            and removing_icc
            and target not in ("srgb", "grayscale")
        ):
            message = "Removing ICC profile may affect color accuracy."
            warnings.append(message)
            metadata_card.set_warning(message)
        else:
            metadata_card.clear_warning()

        if metadata and has_dpi and removing_all:
            message = "Remove All Metadata may also remove DPI information."
            warnings.append(message)
            dpi_card.set_warning(message)
        else:
            dpi_card.clear_warning()
        return warnings

    def validate(self):
        errors = []
        for key, card in self.cards.items():
            if not card.is_enabled():
                continue
            valid, message = card.option_widget.validate()
            if not valid:
                errors.append(f"{key}: {message}")
        return not errors, "\n".join(errors)

    def get_settings(self):
        return {
            "operations": self.get_operations(),
            "warnings": self.validate_dependencies(),
        }

    def reset(self):
        self._updating = True
        try:
            for card in self.cards.values():
                card.reset()
        finally:
            self._updating = False
        self.emit_settings()

    def emit_settings(self, *_args):
        if not self._updating:
            self.settings_changed.emit(self.get_settings())
