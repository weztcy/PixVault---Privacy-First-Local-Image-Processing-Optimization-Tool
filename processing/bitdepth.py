from pathlib import Path

from PIL import Image



class BitDepthProcessor:



    def process(
        self,
        source_path,
        output_path,
        settings
    ):

        source = Path(source_path)

        output = Path(output_path)


        bit_depth = settings.get(
            "bit_depth",
            8
        )


        with Image.open(source) as image:

            converted = self.convert_bitdepth(
                image,
                bit_depth
            )


            converted.save(
                output
            )


        return output



    def convert_bitdepth(
        self,
        image,
        bit_depth
    ):


        if bit_depth == 8:

            return self.convert_8bit(
                image
            )


        elif bit_depth == 16:

            return self.convert_16bit(
                image
            )


        elif bit_depth == 32:

            return self.convert_32bit(
                image
            )


        return image



    def convert_8bit(
        self,
        image
    ):

        if image.mode in [
            "RGB",
            "RGBA",
            "L"
        ]:

            return image


        return image.convert(
            "RGB"
        )



    def convert_16bit(
        self,
        image
    ):

        if image.mode != "L":

            image = image.convert(
                "L"
            )


        return image.point(
            lambda value:
            value * 257
        ).convert(
            "I;16"
        )



    def convert_32bit(
        self,
        image
    ):

        grayscale = image.convert(
            "L"
        )


        return grayscale.convert(
            "F"
        )