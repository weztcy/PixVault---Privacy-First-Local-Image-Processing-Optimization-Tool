from pathlib import Path

from formats.encoder import EncoderManager





class ImageConverter:



    def __init__(
        self
    ):

        self.encoder = EncoderManager()





    def convert(
        self,
        source_path,
        output_path,
        settings
    ):


        source = Path(
            source_path
        )


        output = Path(
            output_path
        )


        output.parent.mkdir(
            parents=True,
            exist_ok=True
        )



        from PIL import Image


        with Image.open(source) as image:


            result = self.encoder.save(

                image,

                output,

                settings

            )


        return result