import os
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QBoxLayout,
    QButtonGroup,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class OutputSelector(QWidget):
    output_changed = Signal(Path)

    def __init__(self, default_folder=None):
        super().__init__()

        self.custom_folder = None

        self.default_folder = self.resolve_default_folder(default_folder)

        self.setObjectName("output_selector")

        self.setup_ui()
        self.apply_styles()
        self.update_output()

    # =====================
    # DEFAULT OUTPUT FOLDER
    # =====================

    def resolve_default_folder(self, folder):
        if folder is not None and str(folder).strip():
            return Path(folder).expanduser()

        # Detect OneDrive automatically.
        # Environment variables are used
        # rather than a hardcoded username.

        for env_name in (
            "OneDriveConsumer",
            "OneDrive",
            "OneDriveCommercial",
        ):
            onedrive_path = os.environ.get(env_name)

            if onedrive_path:
                return Path(onedrive_path) / "Pictures" / "PixVault Export"

        # Standard OneDrive fallback

        home = Path.home()
        onedrive = home / "OneDrive"

        if onedrive.is_dir():
            return onedrive / "Pictures" / "PixVault Export"

        # Local Pictures fallback

        return home / "Pictures" / "PixVault Export"

    # =====================
    # MAIN USER INTERFACE
    # =====================

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Main card

        self.container = QFrame()
        self.container.setObjectName("output_selector_card")

        self.container.setFixedHeight(420)

        self.container.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        card_layout = QVBoxLayout(self.container)

        card_layout.setContentsMargins(22, 22, 22, 20)
        card_layout.setSpacing(18)

        # Header

        card_layout.addLayout(self.create_header())

        # Output modes

        card_layout.addLayout(self.create_mode_selector())

        # Folder path section

        card_layout.addWidget(self.create_folder_section())

        # Footer information

        self.helper_label = QLabel(
            "Choose where PixVault should save your processed images."
        )

        self.helper_label.setObjectName("output_helper_text")

        self.helper_label.setWordWrap(True)

        card_layout.addWidget(self.helper_label)

        main_layout.addWidget(self.container)

        # Radio connections

        self.default_radio.toggled.connect(self.on_mode_toggled)

        self.custom_radio.toggled.connect(self.on_mode_toggled)

    # =====================
    # PREMIUM HEADER
    # =====================

    def create_header(self):
        header = QHBoxLayout()
        header.setSpacing(12)

        # Header text

        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)

        eyebrow = QLabel("EXPORT DESTINATION")

        eyebrow.setObjectName("output_eyebrow")

        title = QLabel("Output Folder")

        title.setObjectName("output_title")

        description = QLabel("Select the destination for your processed image files.")

        description.setObjectName("output_description")

        description.setWordWrap(True)

        text_layout.addWidget(eyebrow)
        text_layout.addWidget(title)
        text_layout.addWidget(description)

        # Local storage badge

        local_badge = QLabel("●  LOCAL STORAGE")

        local_badge.setObjectName("output_local_badge")

        local_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header.addLayout(text_layout, 1)

        header.addWidget(
            local_badge,
            0,
            Qt.AlignmentFlag.AlignTop,
        )

        return header

    # =====================
    # OUTPUT MODE SELECTOR
    # =====================

    def create_mode_selector(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        label = QLabel("DESTINATION MODE")

        label.setObjectName("output_section_label")

        layout.addWidget(label)

        # Radio button group

        self.radio_group = QButtonGroup(self)
        self.radio_group.setExclusive(True)

        self.default_radio = QRadioButton("Default Folder")

        self.default_radio.setObjectName("output_mode_radio")

        self.default_radio.setMinimumHeight(50)

        self.default_radio.setCursor(Qt.CursorShape.PointingHandCursor)

        self.default_radio.setToolTip(
            "Use PixVault's automatically detected output folder."
        )

        self.custom_radio = QRadioButton("Custom Folder")

        self.custom_radio.setObjectName("output_mode_radio")

        self.custom_radio.setMinimumHeight(50)

        self.custom_radio.setCursor(Qt.CursorShape.PointingHandCursor)

        self.custom_radio.setToolTip(
            "Save processed images to a folder of your choice."
        )

        self.radio_group.addButton(self.default_radio)

        self.radio_group.addButton(self.custom_radio)

        # Default mode

        self.default_radio.setChecked(True)

        # Responsive mode layout

        self.mode_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)

        self.mode_layout.setSpacing(10)

        self.mode_layout.addWidget(
            self.default_radio,
            1,
        )

        self.mode_layout.addWidget(
            self.custom_radio,
            1,
        )

        layout.addLayout(self.mode_layout)

        return layout

    # =====================
    # FOLDER SECTION
    # =====================

    def create_folder_section(self):
        section = QFrame()

        section.setObjectName("output_path_section")

        layout = QVBoxLayout(section)

        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Folder header

        header = QHBoxLayout()
        header.setSpacing(8)

        path_title = QLabel("SELECTED DESTINATION")

        path_title.setObjectName("output_section_label")

        self.mode_badge = QLabel("DEFAULT")

        self.mode_badge.setObjectName("output_mode_badge")

        self.mode_badge.setProperty(
            "mode",
            "default",
        )

        self.mode_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header.addWidget(path_title)
        header.addStretch()
        header.addWidget(self.mode_badge)

        layout.addLayout(header)

        # Folder path field

        self.folder_input = QLineEdit()

        self.folder_input.setObjectName("output_folder_input")

        self.folder_input.setReadOnly(True)

        self.folder_input.setMinimumHeight(44)

        self.folder_input.setPlaceholderText("No output folder selected")

        self.folder_input.setCursor(Qt.CursorShape.IBeamCursor)

        self.folder_input.setAccessibleName("Selected output folder path")

        # Path can be selected and copied
        # despite being read-only.

        layout.addWidget(self.folder_input)

        # Folder actions

        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)

        self.copy_button = QPushButton("Copy Path")

        self.copy_button.setObjectName("output_copy_button")

        self.copy_button.setMinimumHeight(38)

        self.copy_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.copy_button.clicked.connect(self.copy_path)

        self.browse_button = QPushButton("Browse Folder  ↗")

        self.browse_button.setObjectName("output_browse_button")

        self.browse_button.setMinimumHeight(38)

        self.browse_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.browse_button.clicked.connect(self.select_folder)

        action_layout.addStretch()

        action_layout.addWidget(self.copy_button)

        action_layout.addWidget(self.browse_button)

        layout.addLayout(action_layout)

        return section

    # =====================
    # RADIO MODE CHANGED
    # =====================

    def on_mode_toggled(self, checked):
        # Exclusive radio buttons emit both
        # unchecked and checked transitions.
        # Only update for the active option.

        if checked:
            self.update_output()

    # =====================
    # SELECT CUSTOM FOLDER
    # =====================

    def select_folder(self):
        initial_folder = (
            self.custom_folder
            if self.custom_folder is not None
            else self.get_output_folder()
        )

        # QFileDialog should start at an
        # existing directory if possible.

        start_folder = Path(initial_folder).expanduser()

        while not start_folder.is_dir() and start_folder != start_folder.parent:
            start_folder = start_folder.parent

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder",
            str(start_folder),
            QFileDialog.Option.ShowDirsOnly,
        )

        if not folder:
            return

        self.custom_folder = Path(folder).expanduser()

        # If another mode is active, checking
        # this radio button triggers the update.
        # Otherwise, update explicitly.

        if not self.custom_radio.isChecked():
            self.custom_radio.setChecked(True)
        else:
            self.update_output()

    # =====================
    # UPDATE OUTPUT
    # =====================

    def update_output(self):
        folder = self.get_output_folder()

        self.folder_input.setText(str(folder))

        self.folder_input.setToolTip(str(folder))

        # Show the beginning of long paths.

        self.folder_input.setCursorPosition(0)

        self.copy_button.setText("Copy Path")

        # Selected mode information

        if self.custom_radio.isChecked():
            if self.custom_folder is not None:
                mode = "custom"
                mode_text = "CUSTOM"

                helper = (
                    "Processed images will be saved to your selected custom folder."
                )

            else:
                mode = "fallback"
                mode_text = "DEFAULT FALLBACK"

                helper = (
                    "No custom folder has been chosen yet. "
                    "The default destination is currently "
                    "being used. Click Browse Folder "
                    "to select a custom location."
                )

        else:
            mode = "default"
            mode_text = "DEFAULT"

            helper = (
                "PixVault automatically selects an "
                "output folder using your OneDrive "
                "or Pictures directory."
            )

        self.mode_badge.setText(mode_text)

        self.mode_badge.setProperty(
            "mode",
            mode,
        )

        self.mode_badge.style().unpolish(self.mode_badge)

        self.mode_badge.style().polish(self.mode_badge)

        self.mode_badge.update()

        self.helper_label.setText(helper)

        # Preserve the original Path signal.

        self.output_changed.emit(folder)

    # =====================
    # GET OUTPUT FOLDER
    # =====================

    def get_output_folder(self):
        if self.custom_radio.isChecked():
            if self.custom_folder is not None:
                return self.custom_folder

        return self.default_folder

    # =====================
    # GET CURRENT FOLDER
    # =====================

    def get_current_folder(self):
        return self.get_output_folder()

    # =====================
    # SET DEFAULT FOLDER
    # =====================

    def set_default_folder(self, folder):
        self.default_folder = self.resolve_default_folder(folder)

        # The default is also used when
        # Custom mode has no selected folder.

        if self.default_radio.isChecked() or self.custom_folder is None:
            self.update_output()

    # =====================
    # COPY OUTPUT PATH
    # =====================

    def copy_path(self):
        folder = self.get_output_folder()

        clipboard = QApplication.clipboard()

        if clipboard is None:
            return

        clipboard.setText(str(folder))

        self.copy_button.setText("Copied ✓")

    # =====================
    # RESPONSIVE LAYOUT
    # =====================

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if not hasattr(self, "mode_layout"):
            return

        if self.width() < 440:
            self.mode_layout.setDirection(QBoxLayout.Direction.TopToBottom)
        else:
            self.mode_layout.setDirection(QBoxLayout.Direction.LeftToRight)

    # =====================
    # PREMIUM STYLING
    # =====================

    def apply_styles(self):
        self.setStyleSheet(
            """
            /* MAIN COMPONENT */

            QWidget#output_selector {
                background: transparent;
                border: none;
            }

            /* MAIN CARD */

            QFrame#output_selector_card {
                background-color: #141e30;
                border: 1px solid #29374c;
                border-radius: 16px;
            }

            /* HEADER EYEBROW */

            QLabel#output_eyebrow {
                color: #5eead4;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            /* HEADER TITLE */

            QLabel#output_title {
                color: #f1f5f9;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 19px;
                font-weight: 700;
            }

            /* HEADER DESCRIPTION */

            QLabel#output_description {
                color: #94a3b8;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 12px;
            }

            /* LOCAL STORAGE BADGE */

            QLabel#output_local_badge {
                background-color: #173a40;
                color: #5eead4;

                border: 1px solid #28665f;
                border-radius: 8px;

                padding: 7px 11px;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            /* SECTION LABELS */

            QLabel#output_section_label {
                color: #94a3b8;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            /* RADIO MODE CARDS */

            QRadioButton#output_mode_radio {
                background-color: #1b2940;
                color: #d5deea;

                border: 1px solid #304259;
                border-radius: 10px;

                padding: 11px 15px;
                spacing: 12px;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 600;
            }

            QRadioButton#output_mode_radio:hover {
                background-color: #203149;
                color: #f8fafc;

                border: 1px solid #426273;
            }

            QRadioButton#output_mode_radio:checked {
                background-color: #173a40;
                color: #5eead4;

                border: 1px solid #397d76;
                border-left: 3px solid #5eead4;

                font-weight: 700;
            }

            QRadioButton#output_mode_radio:checked:hover {
                background-color: #1c4649;
                color: #99f6e4;

                border: 1px solid #5eead4;
                border-left: 3px solid #5eead4;
            }

            /* RADIO INDICATOR */

            QRadioButton#output_mode_radio::indicator {
                width: 18px;
                height: 18px;

                background-color: #101b2d;

                border: 2px solid #50647c;
                border-radius: 11px;
            }

            QRadioButton#output_mode_radio::indicator:hover {
                border: 2px solid #5eead4;
            }

            QRadioButton#output_mode_radio::indicator:checked {
                background-color: #5eead4;

                border: 5px solid #173a40;
                border-radius: 11px;
            }

            QRadioButton#output_mode_radio:focus {
                border-color: #5eead4;
            }

            /* FOLDER PATH SECTION */

            QFrame#output_path_section {
                background-color: #19283c;

                border: 1px solid #304259;
                border-radius: 11px;
            }

            /* MODE BADGES */

            QLabel#output_mode_badge {
                border-radius: 7px;

                padding: 5px 10px;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
            }

            QLabel#output_mode_badge[mode="default"] {
                background-color: #263449;
                color: #cbd5e1;
                border: 1px solid #394a61;
            }

            QLabel#output_mode_badge[mode="custom"] {
                background-color: #173e43;
                color: #5eead4;
                border: 1px solid #28665f;
            }

            QLabel#output_mode_badge[mode="fallback"] {
                background-color: #443820;
                color: #fcd34d;
                border: 1px solid #77602a;
            }

            /* FOLDER PATH INPUT */

            QLineEdit#output_folder_input {
                background-color: #101b2d;

                color: #d5deea;

                border: 1px solid #304259;
                border-radius: 9px;

                padding: 10px 13px;

                font-family: "Consolas";
                font-size: 12px;

                selection-background-color: #285d60;
                selection-color: #f8fafc;
            }

            QLineEdit#output_folder_input:hover {
                border: 1px solid #426273;
            }

            QLineEdit#output_folder_input:focus {
                border: 1px solid #5eead4;
            }

            /* COPY PATH BUTTON */

            QPushButton#output_copy_button {
                background-color: #1b2940;
                color: #d5deea;

                border: 1px solid #38536b;
                border-radius: 9px;

                padding: 8px 16px;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 600;
            }

            QPushButton#output_copy_button:hover {
                background-color: #24384e;
                color: #f8fafc;
                border-color: #5eead4;
            }

            QPushButton#output_copy_button:pressed {
                background-color: #285d60;
            }

            /* BROWSE BUTTON */

            QPushButton#output_browse_button {
                background-color: #5eead4;
                color: #0b1120;

                border: 1px solid #5eead4;
                border-radius: 9px;

                padding: 8px 18px;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 700;
            }

            QPushButton#output_browse_button:hover {
                background-color: #99f6e4;
                border-color: #99f6e4;
            }

            QPushButton#output_browse_button:pressed {
                background-color: #2dd4bf;
                border-color: #2dd4bf;
            }

            /* KEYBOARD FOCUS */

            QPushButton#output_copy_button:focus,
            QPushButton#output_browse_button:focus {
                border: 2px solid #99f6e4;
            }

            /* HELPER TEXT */

            QLabel#output_helper_text {
                color: #64748b;
                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 11px;
            }

            /* DISABLED STATES */

            QRadioButton#output_mode_radio:disabled,
            QPushButton#output_copy_button:disabled,
            QPushButton#output_browse_button:disabled {
                background-color: #202b3b;
                color: #64748b;
                border: 1px solid #354459;
            }

            QLineEdit#output_folder_input:disabled {
                background-color: #151e2d;
                color: #64748b;
                border: 1px solid #253348;
            }
            """
        )
