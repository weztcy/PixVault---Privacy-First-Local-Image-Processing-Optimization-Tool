from PySide6.QtCore import QObject, Signal

from core.worker import WorkerThread


class BatchService(QObject):
    progress_changed = Signal(int, int, str, str)

    processing_finished = Signal(dict)

    processing_error = Signal(str)

    processing_cancelled = Signal()

    def __init__(self):

        super().__init__()

        self.thread = None

    def start_batch(self, files, output_folder, config):

        if self.is_running():
            raise RuntimeError("Batch processing is already running")

        if not files:
            raise ValueError("No files provided")

        if not output_folder:
            raise ValueError("Output folder is required")

        if not config:
            raise ValueError("Processing configuration missing")

        self.thread = WorkerThread(files, output_folder, config)

        self.connect_thread()

        self.thread.start()

    def connect_thread(self):

        if not self.thread:
            return

        self.thread.progress_changed.connect(self.progress_changed.emit)

        self.thread.processing_finished.connect(self.on_finished)

        self.thread.processing_error.connect(self.on_error)

        self.thread.finished.connect(self.cleanup_thread)

    def cancel(self):

        if not self.thread:
            return

        if self.thread.isRunning():
            self.thread.cancel()

            self.processing_cancelled.emit()

    def on_finished(self, result):

        self.processing_finished.emit(result)

    def on_error(self, error):

        self.processing_error.emit(error)

    def is_running(self):

        if not self.thread:
            return False

        return self.thread.isRunning()

    def cleanup_thread(self):

        if not self.thread:
            return

        self.thread.deleteLater()

        self.thread = None
