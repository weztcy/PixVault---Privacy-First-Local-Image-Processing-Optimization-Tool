from PIL import Image, ImageCms





class ColorSpaceProcessor:



    PROFILES = {


        "srgb":

            "sRGB",


        "adobe_rgb":

            "Adobe RGB (1998)",


        "display_p3":

            "DisplayP3"

    }







    INTENTS = {


        "perceptual":

            ImageCms.Intent.PERCEPTUAL,


        "relative_colorimetric":

            ImageCms.Intent.RELATIVE_COLORIMETRIC,


        "saturation":

            ImageCms.Intent.SATURATION,


        "absolute_colorimetric":

            ImageCms.Intent.ABSOLUTE_COLORIMETRIC

    }









    def process(
        self,
        image,
        settings
    ):


        target = settings.get(

            "target",

            "sRGB"

        )


        intent = settings.get(

            "intent",

            "perceptual"

        )



        return self.convert_colorspace(

            image,

            target,

            intent

        )









    def convert_colorspace(
        self,
        image,
        target,
        intent
    ):


        target = str(

            target

        ).lower().strip()



        intent = str(

            intent

        ).lower().strip()





        if target == "grayscale":


            return image.convert(

                "L"

            )







        if target == "cmyk":


            return self.convert_cmyk(

                image,

                intent

            )







        if target in self.PROFILES:


            return self.convert_icc(

                image,

                target,

                intent

            )






        raise ValueError(

            f"Unsupported color space: {target}"

        )









    def convert_icc(
        self,
        image,
        target,
        intent
    ):


        source_profile = image.info.get(

            "icc_profile"

        )



        if source_profile:


            input_profile = ImageCms.ImageCmsProfile(

                bytes(source_profile)

            )


        else:


            input_profile = ImageCms.createProfile(

                "sRGB"

            )






        output_profile = ImageCms.createProfile(

            self.PROFILES[target]

        )





        transform = ImageCms.buildTransform(

            input_profile,

            output_profile,

            image.mode,

            image.mode,

            renderingIntent=self.INTENTS.get(

                intent,

                ImageCms.Intent.PERCEPTUAL

            )

        )






        result = ImageCms.applyTransform(

            image,

            transform

        )





        result.info["icc_profile"] = ImageCms.ImageCmsProfile(

            output_profile

        ).tobytes()





        return result










    def convert_cmyk(
        self,
        image,
        intent
    ):


        rgb = image.convert(

            "RGB"

        )



        rgb_profile = ImageCms.createProfile(

            "sRGB"

        )



        cmyk_profile = ImageCms.createProfile(

            "CMYK"

        )





        transform = ImageCms.buildTransform(

            rgb_profile,

            cmyk_profile,

            "RGB",

            "CMYK",

            renderingIntent=self.INTENTS.get(

                intent,

                ImageCms.Intent.PERCEPTUAL

            )

        )





        return ImageCms.applyTransform(

            rgb,

            transform

        )