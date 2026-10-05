from core.worker import WorkerThread



class BatchService:



    def __init__(self):

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


        self.thread = WorkerThread(
            files,
            output_folder,
            config
        )


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


        self.thread.start()



    def cancel(self):

        if self.thread:

            self.thread.cancel()