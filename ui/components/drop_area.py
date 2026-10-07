from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor, QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import QFileDialog, QLabel, QVBoxLayout, QWidget


class DropArea(QWidget):
    files_dropped = Signal(list)

    SUPPORTED_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".avif",
        ".gif",
        ".bmp",
        ".tiff",
        ".tif",
        ".heic",
        ".heif",
        ".ico",
        ".svg",
    }

    def __init__(self):

        super().__init__()

        self.setAcceptDrops(True)

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel("📂 Click or Drag & Drop Images / Folder Here")

        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label.setMinimumHeight(120)

        self.label.setObjectName("drop_area")

        self.label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.label.setStyleSheet(
            """
            QLabel#drop_area
            {
                border: 2px dashed #888888;
                border-radius: 10px;
                background-color: rgba(120,120,120,0.05);
                color: #555555;
                font-size: 14px;
            }


            QLabel#drop_area:hover
            {
                border: 2px dashed #4a90e2;
                background-color: rgba(74,144,226,0.08);
            }


            QLabel#drop_area:pressed
            {
                border: 2px dashed #2c6cb0;
                background-color: rgba(74,144,226,0.15);
            }
            """
        )

        layout.addWidget(self.label)

        self.setLayout(layout)

    # =====================
    # CLICK IMPORT
    # =====================

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:
            self.open_file_dialog()

        super().mousePressEvent(event)

    def open_file_dialog(self):

        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images",
            "",
            (
                "Images "
                "(*.jpg *.jpeg *.png *.webp *.avif "
                "*.gif *.bmp *.tiff *.tif "
                "*.heic *.heif *.ico *.svg)"
            ),
        )

        result = []

        for file in files:
            path = Path(file)

            if self.is_supported_image(path):
                result.append(path)

        if result:
            self.files_dropped.emit(result)

    # =====================
    # DRAG DROP
    # =====================

    def dragEnterEvent(self, event: QDragEnterEvent):

        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):

        urls = event.mimeData().urls()

        files = []

        for url in urls:
            path = Path(url.toLocalFile())

            if path.is_file():
                if self.is_supported_image(path):
                    files.append(path)

            elif path.is_dir():
                files.extend(self.scan_folder(path))

        if files:
            self.files_dropped.emit(files)

        event.acceptProposedAction()

    def scan_folder(self, folder):

        result = []

        for file in folder.rglob("*"):
            if file.is_file():
                if self.is_supported_image(file):
                    result.append(file)

        return result

    def is_supported_image(self, path):

        return path.suffix.lower() in self.SUPPORTED_EXTENSIONS
