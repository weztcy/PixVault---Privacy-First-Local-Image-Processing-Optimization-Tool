from pathlib import Path

from PIL import Image

from formats import BaseEncoder



class AVIFEncoder(BaseEncoder):


    def save(
        self,
        image,
        output_path,
        settings
    ):

        output = Path(output_path)


        lossless = settings.get(
            "lossless",
            False
        )


        quality = settings.get(
            "quality",
            80
        )


        speed = settings.get(
            "speed",
            6
        )


        subsampling = settings.get(
            "subsampling",
            "4:2:0"
        )


        image.save(
            output,
            format="AVIF",
            lossless=lossless,
            quality=quality,
            speed=speed,
            subsampling=subsampling
        )


        return output