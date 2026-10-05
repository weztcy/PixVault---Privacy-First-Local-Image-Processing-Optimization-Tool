from pathlib import Path

from PIL import Image

from formats import BaseEncoder



class BMPEncoder(BaseEncoder):


    def save(
        self,
        image,
        output_path,
        settings
    ):

        output = Path(output_path)


        bit_depth = settings.get(
            "bit_depth",
            24
        )


        image = self.prepare_image(
            image,
            bit_depth
        )


        image.save(
            output,
            format="BMP"
        )


        return output



    def prepare_image(
        self,
        image,
        bit_depth
    ):


        if bit_depth == 32:

            return image.convert(
                "RGBA"
            )


        elif bit_depth == 24:

            return image.convert(
                "RGB"
            )


        elif bit_depth == 8:

            return image.convert(
                "P"
            )


        elif bit_depth in [
            1,
            4
        ]:

            return image.convert(
                "1"
            )


        elif bit_depth == 16:

            return image.convert(
                "RGB"
            )


        return image.convert(
            "RGB"
        )