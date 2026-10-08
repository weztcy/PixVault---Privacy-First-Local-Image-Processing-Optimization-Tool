from PySide6.QtCore import Signal
from PySide6.QtWidgets import QScrollArea, QVBoxLayout, QWidget

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

        self.setup_ui()

    def setup_ui(self):

        root = QVBoxLayout(self)

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(True)

        self.container = QWidget()

        self.layout = QVBoxLayout(self.container)

        self.layout.setSpacing(12)

        self.scroll.setWidget(self.container)

        root.addWidget(self.scroll)

        self.create_cards()

    def create_cards(self):

        for key, data in self.PROCESSORS.items():
            title, widget_class = data

            option_widget = widget_class()

            card = ProcessingCard(title, option_widget)

            card.settings_changed.connect(self.emit_settings)

            self.cards[key] = card

            self.layout.addWidget(card)

    def set_format(self, format_name):

        self.current_format = format_name.upper()

        for card in self.cards.values():
            widget = card.option_widget

            widget.current_format = self.current_format

            if hasattr(widget, "update_capability"):
                widget.update_capability()

        self.validate_dependencies()

        self.emit_settings()

    def get_operations(self):

        operations = []

        for card in self.cards.values():
            settings = card.get_settings()

            if settings:
                operations.append(settings)

        return operations

    def validate_dependencies(self):

        warnings = []

        colorspace = self.cards["colorspace"].option_widget.get_settings()

        metadata = self.cards["metadata"].option_widget.get_settings()

        if colorspace.get("target") not in [
            None,
            "sRGB",
        ] and "ICC Profile" in metadata.get("remove", []):
            warning = "Removing ICC Profile may affect color accuracy."

            warnings.append(warning)

            self.cards["metadata"].set_warning(warning)

        else:
            self.cards["metadata"].clear_warning()

        if metadata.get("mode") == "all":
            dpi_warning = "Remove All Metadata may remove DPI information."

            warnings.append(dpi_warning)

            self.cards["dpi"].set_warning(dpi_warning)

        else:
            self.cards["dpi"].clear_warning()

        return warnings

    def get_settings(self):

        return {
            "operations": self.get_operations(),
            "warnings": self.validate_dependencies(),
        }

    def reset(self):

        for card in self.cards.values():
            card.reset()

        self.emit_settings()

    def emit_settings(self):

        self.settings_changed.emit(self.get_settings())
