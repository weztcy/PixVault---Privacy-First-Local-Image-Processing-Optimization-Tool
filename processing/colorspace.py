from pathlib import Path

from PIL import Image



class ColorSpaceProcessor:



    def process(
        self,
        source_path,
        output_path,
        settings
    ):

        source = Path(source_path)

        output = Path(output_path)


        target = settings.get(
            "target",
            "sRGB"
        )


        with Image.open(source) as image:

            converted = self.convert_colorspace(
                image,
                target
            )


            converted.save(
                output
            )


        return output



    def convert_colorspace(
        self,
        image,
        target
    ):

        target = target.lower()



        if target == "grayscale":

            return image.convert(
                "L"
            )



        elif target == "cmyk":

            return image.convert(
                "CMYK"
            )



        elif target in [
            "srgb",
            "adobe rgb",
            "display p3"
        ]:

            return image.convert(
                "RGB"
            )



        return image