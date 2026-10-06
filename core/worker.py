from pathlib import Path


from PySide6.QtCore import (
    QThread,
    Signal
)


from core.pipeline import ImagePipeline
from export.naming import NamingEngine





class BatchWorker:



    def __init__(
        self
    ):


        self.naming = NamingEngine()








    def run(
        self,
        files,
        output_folder,
        config,
        progress_callback=None,
        cancel_check=None
    ):


        if not files:

            raise ValueError(
                "No files to process"
            )



        output_folder = Path(
            output_folder
        )



        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )



        results = {


            "success": [],


            "failed": [],


            "cancelled": False,


            "total": len(files),


            "processed": 0

        }



        total = len(files)





        for index, file in enumerate(files):


            source = Path(
                file
            )



            # =====================
            # CANCEL
            # =====================

            if cancel_check and cancel_check():


                results["cancelled"] = True



                if progress_callback:


                    progress_callback(

                        index,

                        total,

                        source.name,

                        "Cancelled"

                    )


                break





            try:



                if not source.exists():


                    raise FileNotFoundError(

                        f"File not found: {source}"

                    )





                if progress_callback:


                    progress_callback(

                        index,

                        total,

                        source.name,

                        "Processing"

                    )





                output_path = self.create_output_path(

                    source,

                    output_folder,

                    config

                )





                pipeline = ImagePipeline()



                result = pipeline.run(

                    source,

                    output_path,

                    config

                )





                results["success"].append(

                    str(result)

                )





                status = "Completed"






            except Exception as error:



                results["failed"].append(

                    {


                        "file":

                            str(source),


                        "error":

                            str(error)

                    }

                )



                status = "Failed"







            finally:



                results["processed"] = index + 1




                if progress_callback:


                    progress_callback(

                        index + 1,

                        total,

                        source.name,

                        status

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



        if not output_settings:


            raise ValueError(

                "Output configuration missing"

            )





        format_name = output_settings.get(

            "format"

        )





        #
        # keep original format
        #

        if output_settings.get(

            "keep_format"

        ):


            extension = source.suffix.replace(

                ".",

                ""

            )



        else:


            if not format_name:


                raise ValueError(

                    "Output format missing"

                )



            extension = self.naming.normalize_extension(

                format_name

            )







        filename = (

            source.stem

            +

            "_processed"

            +

            "."

            +

            extension

        )



        return output_folder / filename
















class WorkerThread(QThread):



    progress_changed = Signal(

        int,

        int,

        str,

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







    def run(
        self
    ):


        self._cancelled = False



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
        filename,
        status
    ):


        self.progress_changed.emit(

            current,

            total,

            filename,

            status

        )








    def cancel(
        self
    ):


        self._cancelled = True







    def is_cancelled(
        self
    ):


        return self._cancelled