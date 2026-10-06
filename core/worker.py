from pathlib import Path

from PySide6.QtCore import (
    QThread,
    Signal
)


from core.pipeline import ImagePipeline
from export.naming import NamingEngine





class BatchWorker:



    def __init__(self):


        self.naming = NamingEngine()







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


            "failed": [],


            "cancelled": False,


            "total": len(files),


            "processed": 0

        }





        total = len(files)





        for index, file in enumerate(files):



            # =====================
            # CANCEL CHECK
            # =====================


            if cancel_check and cancel_check():


                results["cancelled"] = True


                break





            source = Path(
                file
            )



            try:



                if not source.exists():


                    raise FileNotFoundError(

                        f"File not found: {source}"

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





            except Exception as error:



                results["failed"].append(

                    {


                        "file":

                            str(source),


                        "error":

                            str(error)

                    }

                )






            finally:



                results["processed"] = index + 1





                if progress_callback:


                    progress_callback(

                        index + 1,

                        total,

                        source.name,

                        results

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





        # hanya kandidat awal
        # collision ditangani NamingEngine
        # saat export


        format_name = output_settings.get(

            "format"

        )



        if not format_name:


            raise ValueError(

                "Output format missing"

            )





        extension = self.naming.normalize_extension(

            format_name

        )






        return output_folder / (

            f"{source.stem}.{extension}"

        )









class WorkerThread(QThread):



    progress_changed = Signal(

        int,

        int,

        str,

        dict

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
        results
    ):


        self.progress_changed.emit(

            current,

            total,

            filename,

            results

        )







    def cancel(
        self
    ):


        self._cancelled = True







    def is_cancelled(
        self
    ):


        return self._cancelled