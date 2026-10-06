from pathlib import Path

from PIL import Image





class DPIProcessor:



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



        horizontal, vertical = self.get_dpi(
            settings
        )



        with Image.open(source) as image:


            image.save(

                output,

                format="TIFF",

                compression="tiff_lzw",

                dpi=(

                    horizontal,

                    vertical

                )

            )



        return output







    def get_dpi(
        self,
        settings
    ):


        unit = str(

            settings.get(

                "unit",

                "dpi"

            )

        ).lower()



        horizontal = settings.get(
            "horizontal"
        )


        vertical = settings.get(
            "vertical"
        )



        if horizontal is None:


            horizontal = settings.get(

                "value",

                settings.get(

                    "dpi",

                    300

                )

            )



        if vertical is None:


            vertical = horizontal



        try:


            horizontal = float(
                horizontal
            )


            vertical = float(
                vertical
            )


        except Exception:


            raise ValueError(
                "Invalid DPI value"
            )



        if horizontal <= 0 or vertical <= 0:

            raise ValueError(
                "DPI must be greater than zero"
            )





        if unit == "dpcm":


            horizontal *= 2.54

            vertical *= 2.54



        elif unit != "dpi":

            raise ValueError(

                f"Unsupported DPI unit: {unit}"

            )



        return (

            horizontal,

            vertical

        )