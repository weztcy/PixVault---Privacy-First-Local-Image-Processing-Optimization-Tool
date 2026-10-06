from core.worker import WorkerThread





class BatchService:



    def __init__(
        self
    ):


        self.thread = None







    def start_batch(
        self,
        files,
        output_folder,
        config,
        progress_callback=None,
        finished_callback=None,
        error_callback=None
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







        # =====================
        # SIGNAL CONNECTION
        # =====================



        if progress_callback:


            self.thread.progress_changed.connect(

                progress_callback

            )





        if finished_callback:


            self.thread.processing_finished.connect(

                finished_callback

            )





        if error_callback:


            self.thread.processing_error.connect(

                error_callback

            )







        self.thread.finished.connect(

            self.cleanup_thread

        )





        self.thread.start()







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