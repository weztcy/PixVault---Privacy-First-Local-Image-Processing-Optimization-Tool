from pathlib import Path

from PIL import Image

import pillow_heif

from formats import BaseEncoder


pillow_heif.register_heif_opener()



class HEICEncoder(BaseEncoder):


    def save(
        self,
        image,
        output_path,
        settings
    ):

        output = Path(output_path)


        quality = settings.get(
            "quality",
            85
        )


        lossless = settings.get(
            "lossless",
            False
        )


        bit_depth = settings.get(
            "bit_depth",
            8
        )


        image.save(
            output,
            format="HEIF",
            quality=quality,
            lossless=lossless,
            bit_depth=bit_depth
        )


        return output