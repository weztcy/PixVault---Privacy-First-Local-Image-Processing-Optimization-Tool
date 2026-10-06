from pathlib import Path

from PIL import Image


from processing.resize import ImageResizer
from processing.crop import ImageCropper
from processing.transform import ImageTransformer
from processing.compression import ImageCompressor
from processing.dpi import DPIProcessor
from processing.colorspace import ColorSpaceProcessor
from processing.bitdepth import BitDepthProcessor
from processing.metadata import MetadataProcessor


from export.exporter import Exporter
from history.manager import HistoryManager





class ImagePipeline:



    def __init__(
        self
    ):


        self.processors = {


            "resize":

                ImageResizer(),


            "crop":

                ImageCropper(),


            "transform":

                ImageTransformer(),


            "compression":

                ImageCompressor(),


            "dpi":

                DPIProcessor(),


            "colorspace":

                ColorSpaceProcessor(),


            "bitdepth":

                BitDepthProcessor(),


            "metadata":

                MetadataProcessor()

        }



        self.exporter = Exporter()

        self.history = HistoryManager()

        self.temp_files = []







    def run(
        self,
        source_path,
        output_path,
        config
    ):



        self.temp_files.clear()



        source_path = Path(
            source_path
        )


        output_path = Path(
            output_path
        )




        if not source_path.exists():

            raise FileNotFoundError(

                f"Input file not found: {source_path}"

            )




        if not config:

            raise ValueError(

                "Pipeline configuration missing"

            )




        output_path.parent.mkdir(

            parents=True,

            exist_ok=True

        )




        operations = config.get(

            "operations",

            []

        )



        output_settings = config.get(

            "output"

        )



        if not output_settings:


            raise ValueError(

                "Output configuration missing"

            )




        self.validate_output_format(

            output_settings

        )





        current_file = source_path





        try:




            # =====================
            # PROCESSING CHAIN
            # =====================


            for index, operation in enumerate(

                operations

            ):



                if not isinstance(

                    operation,

                    dict

                ):


                    raise ValueError(

                        "Invalid operation configuration"

                    )





                operation_type = operation.get(

                    "type"

                )




                if not operation_type:


                    raise ValueError(

                        "Operation type missing"

                    )





                processor = self.processors.get(

                    operation_type

                )




                if processor is None:


                    raise ValueError(

                        f"Unsupported operation: {operation_type}"

                    )






                temp_output = self.generate_temp_path(

                    output_path,

                    index

                )




                self.temp_files.append(

                    temp_output

                )





                current_file = processor.process(

                    current_file,

                    temp_output,

                    operation

                )






            # =====================
            # EXPORT
            # =====================



            with Image.open(

                current_file

            ) as image:



                image.load()



                export_result = self.exporter.export(

                    image,

                    source_path,

                    output_path.parent,

                    output_settings

                )






            final_path = Path(

                export_result["path"]

            )






            self.history.add(

                source=str(

                    source_path

                ),


                output=str(

                    final_path

                ),


                format_name=export_result.get(

                    "format"

                ),


                operations=operations,


                status="success"

            )





            return final_path







        except Exception as error:




            self.history.add(

                source=str(

                    source_path

                ),


                output=str(

                    output_path

                ),


                format_name=output_settings.get(

                    "format"

                ),


                operations=operations,


                status="failed",


                error=str(

                    error

                )

            )



            raise






        finally:


            self.cleanup_temp()







    def validate_output_format(
        self,
        output_settings
    ):


        format_name = output_settings.get(

            "format"

        )



        if not format_name:


            raise ValueError(

                "Output format missing"

            )





        if not self.exporter.encoder.is_supported(

            format_name

        ):


            raise ValueError(

                f"Unsupported output format: {format_name}"

            )









    def generate_temp_path(
        self,
        output_path,
        index
    ):



        output_path = Path(

            output_path

        )



        return output_path.parent / (

            f"_pixvault_temp_{index}_"

            f"{output_path.stem}.tiff"

        )








    def cleanup_temp(
        self
    ):



        for file in self.temp_files:



            try:


                file = Path(

                    file

                )



                if file.exists():


                    file.unlink()



            except Exception:


                pass




        self.temp_files.clear()