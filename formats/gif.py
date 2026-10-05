from pathlib import Path

from PIL import Image

from formats import BaseEncoder



class GIFEncoder(BaseEncoder):


    def save(
        self,
        image,
        output_path,
        settings
    ):

        output = Path(output_path)


        colors = settings.get(
            "colors",
            256
        )


        transparency = settings.get(
            "transparency",
            False
        )


        loop = settings.get(
            "loop",
            0
        )


        duration = settings.get(
            "duration",
            100
        )


        if image.mode not in [
            "P",
            "RGBA"
        ]:

            image = image.convert(
                "RGBA"
            )


        if colors:

            image = image.convert(
                "P",
                colors=colors
            )


        save_settings = {

            "format": "GIF",

            "loop": loop,

            "duration": duration

        }


        if transparency:

            save_settings[
                "transparency"
            ] = 0


        image.save(
            output,
            **save_settings
        )


        return output