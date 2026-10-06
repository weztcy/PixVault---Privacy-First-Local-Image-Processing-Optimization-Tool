from pathlib import Path

from PIL import Image





class BitDepthProcessor:



    def process(
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



        value = settings.get(
            "value",
            settings.get(
                "bit_depth",
                8
            )
        )



        try:

            bit_depth = int(
                value
            )

        except Exception:

            raise ValueError(
                "Invalid bit depth value"
            )



        with Image.open(source) as image:


            converted = self.convert_bitdepth(

                image,

                bit_depth

            )



            converted.save(

                output,

                format="TIFF",

                compression="tiff_lzw"

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



        if bit_depth == 16:

            return self.convert_16bit(
                image
            )



        if bit_depth == 32:

            return self.convert_32bit(
                image
            )



        raise ValueError(

            f"Unsupported bit depth: {bit_depth}"

        )








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


        if image.mode == "I;16":

            return image



        grayscale = image.convert(
            "L"
        )



        return grayscale.point(

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