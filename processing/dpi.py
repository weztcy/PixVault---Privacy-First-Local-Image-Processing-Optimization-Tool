from pathlib import Path

from PIL import Image



class DPIProcessor:


    def process(
        self,
        source_path,
        output_path,
        settings
    ):

        source = Path(source_path)

        output = Path(output_path)


        unit = settings.get(
            "unit",
            "dpi"
        )


        horizontal = settings.get(
            "horizontal",
            72
        )


        vertical = settings.get(
            "vertical",
            horizontal
        )


        if unit == "dpcm":

            horizontal = horizontal * 2.54

            vertical = vertical * 2.54



        with Image.open(source) as image:

            image.save(
                output,
                dpi=(
                    horizontal,
                    vertical
                )
            )


        return output