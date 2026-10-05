from pathlib import Path


from core.pipeline import ImagePipeline




class ImageService:



    def __init__(self):

        self.pipeline = ImagePipeline()



    def process_image(
        self,
        source_path,
        output_path,
        config
    ):

        source = Path(
            source_path
        )


        output = Path(
            output_path
        )


        result = self.pipeline.run(
            source,
            output,
            config
        )


        return result



    def validate_input(
        self,
        file_path
    ):


        path = Path(
            file_path
        )


        return (

            path.exists()

            and

            path.is_file()

        )