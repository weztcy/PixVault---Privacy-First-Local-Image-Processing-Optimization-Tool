from pathlib import Path

from PIL import Image

from formats import BaseEncoder



class WEBPEncoder(BaseEncoder):


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
            85
        )


        method = settings.get(
            "method",
            4
        )


        alpha_quality = settings.get(
            "alpha_quality",
            100
        )


        image.save(
            output,
            format="WEBP",
            lossless=lossless,
            quality=quality,
            method=method,
            alpha_quality=alpha_quality
        )


        return output