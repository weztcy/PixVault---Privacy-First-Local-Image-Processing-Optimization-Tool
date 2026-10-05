from pathlib import Path

from PIL import Image

from formats import BaseEncoder



class ICOEncoder(BaseEncoder):


    def save(
        self,
        image,
        output_path,
        settings
    ):

        output = Path(output_path)


        size = settings.get(
            "size",
            256
        )


        transparency = settings.get(
            "transparency",
            True
        )


        image = self.prepare_image(
            image,
            size,
            transparency
        )


        image.save(
            output,
            format="ICO",
            sizes=[
                (
                    size,
                    size
                )
            ]
        )


        return output



    def prepare_image(
        self,
        image,
        size,
        transparency
    ):

        image = image.convert(
            "RGBA"
        )


        image = image.resize(
            (
                size,
                size
            ),
            Image.Resampling.LANCZOS
        )


        if not transparency:

            background = Image.new(
                "RGB",
                image.size,
                "white"
            )

            background.paste(
                image,
                mask=image.getchannel("A")
            )

            return background


        return image