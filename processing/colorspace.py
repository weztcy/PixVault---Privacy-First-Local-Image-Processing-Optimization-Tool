from pathlib import Path

from PIL import Image, ImageCms





class ColorSpaceProcessor:



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



        target = settings.get(

            "target",

            "sRGB"

        )



        with Image.open(source) as image:


            converted = self.convert_colorspace(

                image,

                target

            )



            save_settings = {


                "format":

                    "TIFF",


                "compression":

                    "tiff_lzw"

            }



            icc_profile = converted.info.get(
                "icc_profile"
            )



            if icc_profile:


                save_settings["icc_profile"] = icc_profile



            converted.save(

                output,

                **save_settings

            )



        return output







    def convert_colorspace(
        self,
        image,
        target
    ):


        target = str(
            target
        ).lower().strip()





        if target == "srgb":


            return self.convert_srgb(
                image
            )






        if target == "grayscale":


            return image.convert(
                "L"
            )






        if target == "cmyk":


            return image.convert(
                "CMYK"
            )






        raise ValueError(

            f"Unsupported color space: {target}"

        )








    def convert_srgb(
        self,
        image
    ):


        rgb = image.convert(
            "RGB"
        )



        profile = ImageCms.createProfile(
            "sRGB"
        )



        rgb.info["icc_profile"] = (

            ImageCms.ImageCmsProfile(

                profile

            ).tobytes()

        )



        return rgb