from pathlib import Path

from PIL import Image

from formats import BaseEncoder



class PNGEncoder(BaseEncoder):


    def save(
        self,
        image,
        output_path,
        settings
    ):

        output = Path(output_path)


        compression = settings.get(
            "compression",
            6
        )


        interlace = settings.get(
            "interlace",
            False
        )


        image.save(
            output,
            format="PNG",
            compress_level=compression,
            interlace=interlace
        )


        return output