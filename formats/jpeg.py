from pathlib import Path

from PIL import Image

from formats import BaseEncoder



class JPEGEncoder(BaseEncoder):


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


        progressive = settings.get(
            "progressive",
            False
        )


        optimize = settings.get(
            "optimize",
            True
        )


        subsampling = settings.get(
            "subsampling",
            "4:2:0"
        )


        if image.mode in [
            "RGBA",
            "LA"
        ]:

            background = Image.new(
                "RGB",
                image.size,
                "white"
            )

            background.paste(
                image,
                mask=image.getchannel("A")
            )

            image = background


        elif image.mode != "RGB":

            image = image.convert(
                "RGB"
            )


        image.save(
            output,
            format="JPEG",
            quality=quality,
            progressive=progressive,
            optimize=optimize,
            subsampling=subsampling
        )


        return output