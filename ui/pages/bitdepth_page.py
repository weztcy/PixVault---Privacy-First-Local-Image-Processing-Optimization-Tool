"""PixVault bit-depth workspace using the shared ConvertPage visual structure.

The existing backend supports 8-bit output and 16-bit grayscale PNG/TIFF.
32-bit output, and 16-bit multi-channel output, require encoder changes.
"""

from pathlib import Path

from PIL import Image
from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import (
    QBoxLayout,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ui.components.drop_area import DropArea
from ui.components.export_progress import ExportProgress
from ui.components.image_info_panel import ImageInfoPanel
from ui.components.image_list_widget import ImageListWidget
from ui.components.image_preview import ImagePreview
from ui.components.output_selector import OutputSelector
from ui.components.processing_options.bitdepth_options import BitDepthOptions
from ui.components.processing_options.common.format_support_info import (
    FormatSupportInfo,
)
from ui.styles.pixvault_theme import apply_page_theme, role


class BitDepthPage(QWidget):
    """Consistent PixVault page for bit-depth conversion and batch exporting."""

    OUTPUT_FORMATS = ("Same as source", "PNG", "TIFF")
    SOURCE_FORMATS = {
        ".png": "PNG",
        ".tif": "TIFF",
        ".tiff": "TIFF",
    }

    def __init__(self, image_service, batch_service):
        super().__init__()
        self.image_service = image_service
        self.batch_service = batch_service
        self.images = []
        self.output_folder = None
        self._processing_active = False
        self._cancel_requested = False

        self.setObjectName("bitdepth_page")
        role(self, "page")

        self.setup_ui()
        self.apply_styles()
        self.connect_events()
        self.change_format(self.format_box.currentText())
        self.update_queue_state()
        self.update_responsive_layout()

    # =====================
    # WIDGET HELPERS
    # =====================

    def text(self, content, style_role, wrap=False):
        label = role(QLabel(str(content)), style_role)
        label.setWordWrap(wrap)
        label.setTextFormat(Qt.TextFormat.PlainText)
        label.setMinimumWidth(0)
        return label

    def setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.scroll_area = role(QScrollArea(), "pageScroll")
        self.scroll_area.setObjectName("bitdepth_scroll")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.container = role(QWidget(), "pageContainer")
        self.container.setObjectName("bitdepth_container")
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(26, 26, 26, 30)
        self.layout.setSpacing(18)

        self.layout.addWidget(self.create_header())
        self.format_support = FormatSupportInfo("bitdepth")
        self.layout.addWidget(self.format_support)

        # 01 / IMPORT & ORGANIZE
        self.layout.addWidget(
            self.create_section_header(
                "01", "Import & Organize",
                "Add images, manage the queue, and inspect selected files.",
            )
        )
        # DropArea handles both file and folder imports itself.
        self.drop_area = DropArea()
        self.image_list = ImageListWidget()
        self.drop_area.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        self.image_list.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        self.import_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.import_layout.setSpacing(16)
        self.import_layout.addWidget(self.drop_area, 4)
        self.import_layout.addWidget(self.image_list, 6)
        self.layout.addLayout(self.import_layout)

        self.preview = ImagePreview()
        self.info_panel = ImageInfoPanel()
        self.preview.setMinimumWidth(0)
        self.info_panel.setMinimumWidth(0)
        self.preview.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.info_panel.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        self.preview_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.preview_layout.setSpacing(16)
        self.preview_layout.addWidget(self.preview, 6)
        self.preview_layout.addWidget(self.info_panel, 4)
        self.layout.addLayout(self.preview_layout)

        # 02 / BIT DEPTH SETTINGS
        self.layout.addWidget(
            self.create_section_header(
                "02", "Configure Bit Depth",
                "Choose an output format, bit depth, and destination folder.",
            )
        )
        self.settings_box = self.create_settings_card()
        self.output_selector = OutputSelector()
        self.output_folder = self.output_selector.get_output_folder()
        self.settings_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self.settings_layout.setSpacing(16)
        self.settings_layout.addWidget(self.settings_box, 6)
        self.settings_layout.addWidget(self.output_selector, 5)
        self.layout.addLayout(self.settings_layout)

        # 03 / PROCESS & EXPORT
        self.layout.addWidget(
            self.create_section_header(
                "03", "Process & Export",
                "Apply bit-depth settings and monitor batch export progress.",
            )
        )
        self.layout.addWidget(self.create_action_card())
        self.progress = ExportProgress()
        self.layout.addWidget(self.progress)
        self.layout.addStretch(0)

        self.scroll_area.setWidget(self.container)
        self.scroll_area.viewport().installEventFilter(self)
        root.addWidget(self.scroll_area)

    def create_header(self):
        hero = role(QFrame(), "hero")
        layout = QHBoxLayout(hero)
        layout.setContentsMargins(26, 24, 26, 24)
        layout.setSpacing(18)

        heading = QVBoxLayout()
        heading.setSpacing(8)
        heading.addWidget(self.text("PIXVAULT / BIT DEPTH STUDIO", "eyebrow"))
        heading.addWidget(self.text("Adjust Bit Depth", "heroTitle"))
        heading.addWidget(
            self.text(
                "Prepare image bit depth for your workflow with local processing.",
                "heroDescription", True,
            )
        )
        layout.addLayout(heading, 1)

        badges = QVBoxLayout()
        badges.setSpacing(10)
        self.workflow_badge = self.text("READY", "statusBadge")
        self.workflow_badge.setProperty("state", "ready")
        self.workflow_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_count_label = self.text("0 IMAGES", "countBadge")
        self.image_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badges.addWidget(self.workflow_badge)
        badges.addWidget(self.image_count_label)
        layout.addLayout(badges)
        return hero

    def create_section_header(self, number, title, description):
        section = QWidget()
        layout = QHBoxLayout(section)
        layout.setContentsMargins(2, 6, 2, 2)
        layout.setSpacing(14)
        badge = self.text(number, "sectionNumber")
        badge.setFixedSize(40, 40)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading = QVBoxLayout()
        heading.setSpacing(4)
        heading.addWidget(self.text(title, "sectionTitle"))
        heading.addWidget(self.text(description, "sectionDescription", True))
        layout.addWidget(badge)
        layout.addLayout(heading, 1)
        return section

    def create_settings_card(self):
        card = role(QFrame(), "card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(13)
        layout.addWidget(self.text("PIXEL PRECISION", "eyebrow"))
        layout.addWidget(self.text("Bit Depth Settings", "cardTitle"))
        layout.addWidget(
            self.text(
                "Select the precision of the exported image.",
                "description", True,
            )
        )
        layout.addSpacing(5)
        layout.addWidget(self.text("OUTPUT FORMAT", "fieldTitle"))

        self.format_box = role(QComboBox(), "field")
        self.format_box.setObjectName("bitdepth_format_box")
        self.format_box.setMinimumHeight(44)
        self.format_box.setCursor(Qt.CursorShape.PointingHandCursor)
        self.format_box.setAccessibleName("Bit depth output format")
        self.format_box.addItems(self.OUTPUT_FORMATS)
        layout.addWidget(self.format_box)
        self.format_hint = self.text("", "hint", True)
        layout.addWidget(self.format_hint)
        layout.addSpacing(5)

        divider = role(QFrame(), "divider")
        divider.setFixedHeight(1)
        layout.addWidget(divider)
        layout.addWidget(self.text("BIT DEPTH OPTIONS", "fieldTitle"))
        layout.addWidget(
            self.text(
                "8-bit is broadly supported; 16-bit requires grayscale input.",
                "hint", True,
            )
        )

        self.bitdepth_options = BitDepthOptions()
        role(self.bitdepth_options.bit_depth, "field")
        self.bitdepth_options.bit_depth.setMinimumHeight(44)
        self.bitdepth_options.bit_depth.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        for label in self.bitdepth_options.findChildren(QLabel):
            role(
                label,
                "errorText" if label is self.bitdepth_options.warning_label
                else "fieldTitle",
            )
        layout.addWidget(self.bitdepth_options)

        self.capability_hint = self.text(
            "Current encoder support: 8-bit PNG/TIFF; conversion from 8-bit "
            "grayscale to 16-bit grayscale PNG/TIFF. 16-bit RGB and 32-bit "
            "output are not yet supported.",
            "hint", True,
        )
        layout.addWidget(self.capability_hint)
        self.encoding_hint = self.text("", "hint", True)
        layout.addWidget(self.encoding_hint)
        layout.addStretch(0)
        return card

    def create_action_card(self):
        card = role(QFrame(), "card")
        self.action_layout = QBoxLayout(
            QBoxLayout.Direction.LeftToRight, card
        )
        self.action_layout.setContentsMargins(20, 20, 20, 20)
        self.action_layout.setSpacing(18)

        summary = QVBoxLayout()
        summary.setSpacing(6)
        summary.addWidget(self.text("Ready to Adjust Bit Depth?", "cardTitle"))
        self.queue_summary = self.text(
            "Add images to begin.", "description", True
        )
        summary.addWidget(self.queue_summary)
        self.action_layout.addLayout(summary, 1)

        self.action_buttons = QHBoxLayout()
        self.action_buttons.setSpacing(10)
        self.cancel_button = role(QPushButton("Cancel Processing"), "dangerButton")
        self.start_button = role(QPushButton("Apply Bit Depth →"), "primaryButton")
        for button in (self.cancel_button, self.start_button):
            button.setMinimumHeight(46)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_button.hide()
        self.action_buttons.addWidget(self.cancel_button)
        self.action_buttons.addWidget(self.start_button)
        self.action_layout.addLayout(self.action_buttons)
        return card

    # =====================
    # SIGNALS / IMAGE QUEUE
    # =====================

    def connect_events(self):
        self.drop_area.files_dropped.connect(self.load_images)
        self.image_list.image_selected.connect(self.show_preview)
        self.image_list.images_changed.connect(self.on_images_changed)
        self.output_selector.output_changed.connect(self.set_output_folder)
        self.format_box.currentTextChanged.connect(self.change_format)
        self.bitdepth_options.bit_depth.currentTextChanged.connect(
            self.update_queue_state
        )
        self.start_button.clicked.connect(self.start_bitdepth)
        self.cancel_button.clicked.connect(self.cancel_processing)
        self.batch_service.progress_changed.connect(self.on_batch_progress)
        self.batch_service.processing_finished.connect(self.bitdepth_finished)
        self.batch_service.processing_error.connect(self.bitdepth_error)

    def load_images(self, images):
        """Append valid files without resetting existing queue contents."""
        if not images or self._processing_active:
            return
        incoming = []
        for image in images:
            try:
                path = Path(image).expanduser()
                if path.is_file():
                    incoming.append(path)
            except (TypeError, ValueError, OSError):
                continue
        current = [Path(path) for path in self.image_list.get_images()]
        combined = list(dict.fromkeys(current + incoming))
        if combined != current:
            self.image_list.set_images(combined)

    def on_images_changed(self, images):
        self.images = [Path(image) for image in images]
        self.change_format(self.format_box.currentText())
        if not self.images:
            self.preview.clear()
            self.info_panel.clear()
            return

        current = self.preview.current_image
        if current not in self.images:
            current = self.images[0]
            self.show_preview(current)
        if hasattr(self.image_list, "select_image"):
            self.image_list.select_image(
                self.images.index(current), emit_signal=False
            )

    def show_preview(self, image):
        if not image:
            self.preview.clear()
            self.info_panel.clear()
            return
        path = Path(image)
        self.preview.set_image(path)
        self.info_panel.set_image(path)

    def set_output_folder(self, folder):
        self.output_folder = Path(folder) if folder else None
        self.update_queue_state()

    def source_format(self):
        """Resolve a single encoder format for a homogeneous source batch."""
        if not self.images:
            return None
        formats = {
            self.SOURCE_FORMATS.get(Path(path).suffix.lower())
            for path in self.images
        }
        return next(iter(formats)) if len(formats) == 1 else None

    def selected_output_format(self):
        choice = self.format_box.currentText()
        return self.source_format() if choice == "Same as source" else choice.upper()

    def disable_unimplemented_depths(self):
        """Base BitDepthOptions allows TIFF 32-bit; exporter does not."""
        chooser = self.bitdepth_options.bit_depth
        model = chooser.model()
        index = chooser.findText("32-bit")
        if index >= 0 and hasattr(model, "item"):
            item = model.item(index)
            if item is not None:
                item.setEnabled(False)
        if chooser.currentText() == "32-bit":
            chooser.setCurrentText("8-bit")

    def change_format(self, _format_name):
        output_format = self.selected_output_format()
        if self.format_box.currentText() == "Same as source":
            self.format_hint.setText(
                "Same as source requires PNG or TIFF inputs of the same format. "
                "Choose an explicit output format for mixed PNG/TIFF batches."
            )
        else:
            self.format_hint.setText(
                f"All images will be exported as {output_format}."
            )
        self.bitdepth_options.set_format(output_format or "PNG")
        self.disable_unimplemented_depths()
        self.update_queue_state()

    def selected_bit_depth(self):
        return int(self.bitdepth_options.get_settings().get("value", 8))

    def update_queue_state(self, *_args):
        count = len(self.images)
        noun = "image" if count == 1 else "images"
        self.image_count_label.setText(
            f"{count} IMAGE" if count == 1 else f"{count} IMAGES"
        )
        depth = self.selected_bit_depth()
        output_format = self.selected_output_format()
        if depth == 16:
            self.encoding_hint.setText(
                "16-bit output currently accepts 8-bit grayscale (L) sources only. "
                "An 8-bit grayscale source is stored in a 16-bit container; "
                "this does not create additional image detail."
            )
        else:
            self.encoding_hint.setText(
                "8-bit output may change image mode based on the selected encoder."
            )

        if not count:
            self.queue_summary.setText(
                "Import PNG or TIFF images to prepare a bit-depth batch."
            )
            self.start_button.setText("Apply Bit Depth →")
        else:
            self.queue_summary.setText(
                f"{count} {noun} selected · {depth}-bit · "
                f"Output: {output_format or 'choose format'}"
            )
            self.start_button.setText(f"Process {count} {noun.title()} →")
        self.start_button.setEnabled(count > 0 and not self._processing_active)

    # =====================
    # CONFIGURATION / VALIDATION
    # =====================

    def validate_inputs(self, depth):
        """Raise useful errors before starting a background worker."""
        invalid = [
            path.name for path in self.images
            if path.suffix.lower() not in self.SOURCE_FORMATS
        ]
        if invalid:
            raise ValueError(
                "Bit Depth currently supports PNG and TIFF inputs. "
                "Unsupported: " + ", ".join(invalid[:5])
                + (" ..." if len(invalid) > 5 else "")
            )
        if depth == 16:
            not_grayscale = []
            for path in self.images:
                try:
                    with Image.open(path) as image:
                        if image.mode not in ("L",):
                            not_grayscale.append(path.name)
                except Exception as error:
                    raise ValueError(
                        f"Unable to inspect image '{path.name}': {error}"
                    ) from error
            if not_grayscale:
                raise ValueError(
                    "16-bit output currently requires 8-bit grayscale (L) sources. "
                    "Unsupported color images: " + ", ".join(not_grayscale[:5])
                    + (" ..." if len(not_grayscale) > 5 else "")
                )

    def build_config(self):
        output_format = self.selected_output_format()
        if output_format not in {"PNG", "TIFF"}:
            raise ValueError(
                "Choose PNG or TIFF output. 'Same as source' only works "
                "when all files share a supported format."
            )

        operation = dict(self.bitdepth_options.get_settings())
        depth = int(operation.get("value", 8))
        if depth not in (8, 16):
            raise ValueError(
                "32-bit export is not yet supported by the current encoders."
            )
        self.validate_inputs(depth)
        operation["type"] = "bitdepth"

        output = {
            "format": output_format,
            "bit_depth": depth,
            "suffix": "bitdepth",
        }
        if depth == 16:
            # Existing encoders require the target grayscale mode explicitly.
            if output_format == "PNG":
                output["color_type"] = "grayscale"
            else:
                output["color"] = "GRAYSCALE"
        else:
            # Avoid forcing an unnecessary grayscale -> RGB conversion when
            # all selected sources are 8-bit grayscale.
            source_modes = set()
            try:
                for path in self.images:
                    with Image.open(path) as image:
                        source_modes.add(image.mode)
            except Exception:
                source_modes = set()
            if output_format == "PNG":
                if source_modes == {"L"}:
                    output["color_type"] = "grayscale"
                elif source_modes and source_modes.issubset({"RGB", "L", "P"}):
                    output["color_type"] = "rgb"
                else:
                    output["color_type"] = "rgba"
            elif source_modes == {"L"}:
                output["color"] = "GRAYSCALE"
            elif source_modes == {"RGBA"}:
                output["color"] = "RGBA"
            else:
                output["color"] = "RGB"
        return {"operations": [operation], "output": output}

    # =====================
    # PROCESSING STATE
    # =====================

    def set_workflow_status(self, state, text):
        self.workflow_badge.setText(str(text))
        self.workflow_badge.setProperty("state", str(state))
        self.workflow_badge.style().unpolish(self.workflow_badge)
        self.workflow_badge.style().polish(self.workflow_badge)
        self.workflow_badge.update()

    def set_processing_state(self, running):
        self._processing_active = bool(running)
        enabled = not self._processing_active
        for widget in (
            self.drop_area,
            self.image_list,
            self.settings_box,
            self.output_selector,
        ):
            widget.setEnabled(enabled)
        self.cancel_button.setVisible(self._processing_active)
        self.cancel_button.setEnabled(self._processing_active)
        self.update_queue_state()

    # =====================
    # BATCH PROCESSING
    # =====================

    def start_bitdepth(self):
        if self._processing_active:
            return
        self.images = [Path(image) for image in self.image_list.get_images()]
        if not self.images:
            QMessageBox.warning(
                self, "Bit Depth", "Please import at least one image."
            )
            return
        if not self.output_folder:
            QMessageBox.warning(
                self, "Bit Depth", "Please select an output folder."
            )
            return
        if self.batch_service.is_running():
            QMessageBox.warning(
                self, "Processing Busy",
                "Another batch is running. Finish it before starting this batch.",
            )
            return

        try:
            config = self.build_config()
            files = self.images.copy()
            self._cancel_requested = False
            self.progress.reset()
            self.progress.set_output_folder(self.output_folder)
            self.set_processing_state(True)
            self.set_workflow_status("processing", "PROCESSING")
            self.progress.set_status("processing", "Starting...")
            self.batch_service.start_batch(files, self.output_folder, config)
        except Exception as error:
            self.set_processing_state(False)
            self.set_workflow_status("failed", "FAILED")
            self.progress.failed(str(error))
            QMessageBox.critical(self, "Bit Depth Error", str(error))

    def on_batch_progress(self, current, total, filename, status):
        if not self._processing_active:
            return
        self.progress.update_progress(current, total, filename, status)
        if self._cancel_requested:
            self.progress.set_status("cancelled", "Cancelling...")

    def cancel_processing(self):
        if not self._processing_active:
            return
        self._cancel_requested = True
        self.cancel_button.setEnabled(False)
        self.set_workflow_status("cancelled", "CANCELLING")
        self.progress.set_status("cancelled", "Cancelling...")
        try:
            self.batch_service.cancel()
        except Exception as error:
            self._cancel_requested = False
            self.cancel_button.setEnabled(True)
            self.set_workflow_status("processing", "PROCESSING")
            self.progress.set_status("processing", "Processing")
            QMessageBox.critical(self, "Cancellation Error", str(error))

    def bitdepth_finished(self, result):
        if not self._processing_active:
            return
        result = result if isinstance(result, dict) else {}
        successes = result.get("success") or []
        failures = result.get("failed") or []
        cancelled = bool(result.get("cancelled", False))
        self.set_processing_state(False)
        self._cancel_requested = False

        if cancelled:
            self.set_workflow_status("cancelled", "CANCELLED")
            self.progress.set_status("cancelled", "Cancelled")
            self.progress.file_label.setText("Processing was cancelled.")
        elif failures:
            self.set_workflow_status("failed", "NEEDS ATTENTION")
            self.progress.set_status("failed", "Finished with errors")
            self.progress.file_label.setText(
                f"{len(successes)} successful, {len(failures)} failed."
            )
        else:
            self.set_workflow_status("completed", "COMPLETED")
            self.progress.finished()

    def bitdepth_error(self, error):
        if not self._processing_active:
            return
        self.set_processing_state(False)
        self._cancel_requested = False
        self.set_workflow_status("failed", "FAILED")
        self.progress.failed(str(error))

    # =====================
    # RESPONSIVE LAYOUT
    # =====================

    def eventFilter(self, watched, event):
        if (
            watched is self.scroll_area.viewport()
            and event.type() == QEvent.Type.Resize
        ):
            self.update_responsive_layout()
        return super().eventFilter(watched, event)

    def update_responsive_layout(self):
        if not hasattr(self, "settings_layout"):
            return
        width = self.scroll_area.viewport().width()
        direction = (
            QBoxLayout.Direction.LeftToRight
            if width >= 960 else QBoxLayout.Direction.TopToBottom
        )
        for layout in (
            self.import_layout,
            self.preview_layout,
            self.settings_layout,
        ):
            if layout.direction() != direction:
                layout.setDirection(direction)

        action_direction = (
            QBoxLayout.Direction.LeftToRight
            if width >= 620 else QBoxLayout.Direction.TopToBottom
        )
        if self.action_layout.direction() != action_direction:
            self.action_layout.setDirection(action_direction)

    def apply_styles(self):
        apply_page_theme(self)
