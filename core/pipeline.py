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



    def __init__(self):

        self.processors = {

            "resize": ImageResizer(),

            "crop": ImageCropper(),

            "transform": ImageTransformer(),

            "compression": ImageCompressor(),

            "dpi": DPIProcessor(),

            "colorspace": ColorSpaceProcessor(),

            "bitdepth": BitDepthProcessor(),

            "metadata": MetadataProcessor()

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


        source_path = Path(
            source_path
        )


        output_path = Path(
            output_path
        )


        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        current_file = source_path


        operations = config.get(
            "operations",
            []
        )



        try:


            for index, operation in enumerate(operations):


                operation_type = operation.get(
                    "type"
                )


                processor = self.processors.get(
                    operation_type
                )


                if not processor:

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



            output_settings = config.get(
                "output",
                {}
            )



            with Image.open(
                current_file
            ) as image:


                export_result = self.exporter.export(
                    image,
                    source_path,
                    output_path.parent,
                    output_settings
                )



            history_record = self.history.add(

                source=str(
                    source_path
                ),

                output=str(
                    export_result["path"]
                ),

                format_name=export_result["format"],

                operations=operations,

                status="success"

            )



            return Path(
                export_result["path"]
            )



        except Exception as error:


            self.history.add(

                source=str(
                    source_path
                ),

                output=str(
                    output_path
                ),

                format_name=config.get(
                    "output",
                    {}
                ).get(
                    "format"
                ),

                operations=operations,

                status="failed",

                error=str(error)

            )


            raise



        finally:

            self.cleanup_temp()



    def generate_temp_path(
        self,
        output_path,
        index
    ):


        output_path = Path(
            output_path
        )


        return output_path.parent / (

            f"_temp_{index}_{output_path.stem}.png"

        )



    def cleanup_temp(
        self
    ):


        for file in self.temp_files:


            if file.exists():

                file.unlink()



        self.temp_files.clear()