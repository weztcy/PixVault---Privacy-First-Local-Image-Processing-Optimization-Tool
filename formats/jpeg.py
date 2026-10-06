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


        output = Path(
            output_path
        )


        output.parent.mkdir(

            parents=True,

            exist_ok=True

        )



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





        try:


            quality = int(
                quality
            )


        except Exception:


            raise ValueError(

                "Invalid JPEG quality"

            )



        quality = max(

            1,

            min(

                95,

                quality

            )

        )





        subsampling_map = {


            "4:4:4":

                0,


            "4:2:2":

                1,


            "4:2:0":

                2

        }



        subsampling = subsampling_map.get(

            str(subsampling),

            2

        )





        # =====================
        # PREPARE IMAGE
        # =====================


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

                mask=image.getchannel(
                    "A"
                )

            )


            image = background



        elif image.mode != "RGB":


            image = image.convert(

                "RGB"

            )





        save_settings = {


            "format":

                "JPEG",


            "quality":

                quality,


            "progressive":

                bool(progressive),


            "optimize":

                bool(optimize),


            "subsampling":

                subsampling

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