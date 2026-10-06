from pathlib import Path

from PIL import Image





class MetadataProcessor:



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



        mode = settings.get(

            "mode",

            "all"

        )



        with Image.open(source) as image:


            cleaned = self.remove_metadata(

                image,

                mode,

                settings

            )



            save_settings = {


                "format":

                    "TIFF",


                "compression":

                    "tiff_lzw"

            }



            if "icc_profile" in cleaned.info:


                save_settings["icc_profile"] = (

                    cleaned.info["icc_profile"]

                )



            cleaned.save(

                output,

                **save_settings

            )



        return output







    def remove_metadata(
        self,
        image,
        mode,
        settings
    ):



        # =====================
        # PRESERVE
        # =====================


        if mode == "preserve":


            return image.copy()






        # =====================
        # CREATE CLEAN IMAGE
        # =====================


        clean = Image.new(

            image.mode,

            image.size

        )


        clean.putdata(

            list(

                image.getdata()

            )

        )






        if mode == "all":


            return clean







        if mode == "custom":


            remove = settings.get(

                "remove",

                []

            )



            for key, value in image.info.items():


                if key not in remove:


                    clean.info[key] = value



            return clean






        raise ValueError(

            f"Unsupported metadata mode: {mode}"

        )








    def get_metadata(
        self,
        image_path
    ):


        with Image.open(image_path) as image:


            return {


                "format":

                    image.format,


                "mode":

                    image.mode,


                "size":

                    image.size,


                "info":

                    dict(

                        image.info

                    ),


                "exif":

                    dict(

                        image.getexif()

                    )

            }