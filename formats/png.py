from pathlib import Path

from PIL import Image

from formats import BaseEncoder





class PNGEncoder(BaseEncoder):



    def save(
        self,
        image,
        output_path,
        settings
    ):


        output = Path(
            output_path
        )


        output.parent.mkdir(

            parents=True,

            exist_ok=True

        )



        compression = settings.get(

            "compression",

            6

        )


        interlace = settings.get(

            "interlace",

            False

        )


        bit_depth = settings.get(

            "bit_depth",

            8

        )


        color_type = str(

            settings.get(

                "color_type",

                "RGBA"

            )

        ).lower()





        try:


            compression = int(
                compression
            )


            bit_depth = int(
                bit_depth
            )


        except Exception:


            raise ValueError(

                "Invalid PNG settings"

            )



        compression = max(

            0,

            min(

                9,

                compression

            )

        )





        # =====================
        # COLOR TYPE
        # =====================


        if color_type == "rgba":


            if image.mode != "RGBA":

                image = image.convert(
                    "RGBA"
                )



        elif color_type == "rgb":


            if image.mode != "RGB":

                image = image.convert(
                    "RGB"
                )



        elif color_type in [

            "gray",

            "grayscale"

        ]:


            image = image.convert(
                "L"
            )



        else:


            raise ValueError(

                f"Unsupported PNG color type: {color_type}"

            )







        # =====================
        # BIT DEPTH
        # =====================


        if bit_depth == 16:


            if image.mode == "L":


                image = image.convert(
                    "I;16"
                )



            else:


                raise ValueError(

                    "PNG 16-bit is only supported for grayscale images"

                )



        elif bit_depth != 8:


            raise ValueError(

                f"Unsupported PNG bit depth: {bit_depth}"

            )






        save_settings = {


            "format":

                "PNG",


            "compress_level":

                compression,


            "interlace":

                bool(interlace)

        }





        icc_profile = image.info.get(

            "icc_profile"

        )



        if icc_profile:


            save_settings["icc_profile"] = icc_profile






        image.save(

            output,

            **save_settings

        )



        return output