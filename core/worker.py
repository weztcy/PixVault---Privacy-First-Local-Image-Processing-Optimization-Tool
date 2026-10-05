from pathlib import Path


from PySide6.QtCore import (
    QObject,
    QThread,
    Signal
)


from core.pipeline import ImagePipeline




class BatchWorker:



    def __init__(self):

        self.pipeline = ImagePipeline()



    def run(
        self,
        files,
        output_folder,
        config,
        progress_callback=None,
        cancel_check=None
    ):


        output_folder = Path(
            output_folder
        )


        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )


        results = {

            "success": [],

            "failed": []

        }


        total = len(
            files
        )


        for index, file in enumerate(files):


            if cancel_check and cancel_check():

                break



            source = Path(
                file
            )


            try:

                output_path = self.create_output_path(
                    source,
                    output_folder,
                    config
                )


                result = self.pipeline.run(
                    source,
                    output_path,
                    config
                )


                results["success"].append(
                    result
                )



            except Exception as error:

                results["failed"].append(
                    {
                        "file": str(source),

                        "error": str(error)
                    }
                )



            if progress_callback:

                progress_callback(
                    index + 1,
                    total,
                    source.name
                )



        return results



    def create_output_path(
        self,
        source,
        output_folder,
        config
    ):


        output_settings = config.get(
            "output",
            {}
        )


        format_name = output_settings.get(
            "format",
            source.suffix.replace(
                ".",
                ""
            )
        ).lower()



        output_path = output_folder / (
            f"{source.stem}.{format_name}"
        )



        counter = 1


        while output_path.exists():


            output_path = output_folder / (
                f"{source.stem}_{counter:03d}.{format_name}"
            )


            counter += 1



        return output_path





class WorkerThread(QThread):


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
        self,
        files,
        output_folder,
        config
    ):

        super().__init__()


        self.files = files

        self.output_folder = output_folder

        self.config = config


        self.worker = BatchWorker()


        self._cancelled = False



    def run(self):

        try:


            result = self.worker.run(

                self.files,

                self.output_folder,

                self.config,

                progress_callback=self.emit_progress,

                cancel_check=self.is_cancelled

            )


            self.processing_finished.emit(
                result
            )



        except Exception as error:


            self.processing_error.emit(
                str(error)
            )



    def emit_progress(
        self,
        current,
        total,
        filename
    ):

        self.progress_changed.emit(
            current,
            total,
            filename
        )



    def cancel(self):

        self._cancelled = True



    def is_cancelled(
        self
    ):

        return self._cancelled