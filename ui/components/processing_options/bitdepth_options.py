"""Bit depth settings (backend contract: {'type':'bitdepth','value':int})."""
from ui.components.processing_options.base_processing_options import BaseProcessingOptions
from ui.components.processing_options.common.dropdown_field import DropdownField


class BitDepthOptions(BaseProcessingOptions):
    BIT_DEPTHS = ["8-bit", "16-bit", "32-bit"]
    LIMITED = {
        "JPEG": {"16-bit", "32-bit"}, "WEBP": {"16-bit", "32-bit"},
        "GIF": {"16-bit", "32-bit"}, "ICO": {"16-bit", "32-bit"},
        "PNG": {"32-bit"}, "AVIF": {"32-bit"},
        "HEIC": {"32-bit"}, "HEIF": {"32-bit"}, "BMP": {"32-bit"},
    }

    def setup_ui(self):
        super().setup_ui()
        self.bit_depth_field = self.add_widget(DropdownField("Bit Depth", self.BIT_DEPTHS, "8-bit"))
        self.bit_depth = self.bit_depth_field.combo  # compatibility with existing pages
        self.bit_depth.currentTextChanged.connect(self.emit_settings)

    def get_settings(self):
        return {"type": "bitdepth", "value": int(self.bit_depth.currentText().split("-")[0])}

    def reset(self):
        self.bit_depth.setCurrentText("8-bit")
        self.update_capability()

    def update_capability(self):
        restricted = self.LIMITED.get(self.current_format, set())
        model = self.bit_depth.model()
        for i in range(self.bit_depth.count()):
            item = model.item(i)
            if item is not None:
                item.setEnabled(self.bit_depth.itemText(i) not in restricted)
        if self.bit_depth.currentText() in restricted:
            old = self.bit_depth.currentText()
            self.bit_depth.setCurrentText("8-bit")
            self.show_warning(f"{self.current_format} does not support {old}.")
        elif restricted:
            self.show_warning(f"{self.current_format} has limited bit depth support.")
        else:
            self.show_warning("")

    def validate(self):
        if self.bit_depth.currentText() in self.LIMITED.get(self.current_format, set()):
            return False, "The selected bit depth is unavailable for this format."
        # Backend's 16-bit RGB and general 32-bit encoding need additional work.
        return True, ""

    def set_defaults(self, settings):
        value = str((settings or {}).get("value", 8)).replace("-bit", "") + "-bit"
        if value in self.BIT_DEPTHS:
            self.bit_depth.setCurrentText(value)
        self.update_capability()
