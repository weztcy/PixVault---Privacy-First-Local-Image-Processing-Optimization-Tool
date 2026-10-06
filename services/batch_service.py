from PySide6.QtCore import QObject, Signal


from core.worker import WorkerThread





class BatchService(QObject):


    progress_changed = Signal(
        int,
        int,
        str
    )


    processing_finished = Signal(
        dict
    )


    processing_error = Signal(
        str
    )





    def __init__(
        self
    ):

        super().__init__()


        self.thread = None







    def start_batch(
        self,
        files,
        output_folder,
        config
    ):


        if self.is_running():


            raise RuntimeError(

                "Batch processing is already running"

            )



        if not files:


            raise ValueError(

                "No files provided"

            )



        if not output_folder:


            raise ValueError(

                "Output folder is required"

            )



        if not config:


            raise ValueError(

                "Processing configuration missing"

            )





        self.thread = WorkerThread(

            files,

            output_folder,

            config

        )





        self.connect_thread()



        self.thread.start()








    def connect_thread(
        self
    ):


        if not self.thread:

            return



        self.thread.progress_changed.connect(

            self.progress_changed.emit

        )



        self.thread.processing_finished.connect(

            self.processing_finished.emit

        )



        self.thread.processing_error.connect(

            self.processing_error.emit

        )



        self.thread.finished.connect(

            self.cleanup_thread

        )








    def cancel(
        self
    ):


        if not self.thread:

            return



        if self.thread.isRunning():


            self.thread.cancel()







    def is_running(
        self
    ):


        if not self.thread:


            return False



        return self.thread.isRunning()







    def cleanup_thread(
        self
    ):


        if self.thread:


            self.thread.deleteLater()


            self.thread = None