from pathlib import Path

from PIL import Image





class ImageCropper:



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



        with Image.open(source) as image:


            cropped = self.crop_image(
                image,
                settings
            )


            cropped.save(

                output,

                format="TIFF",

                compression="tiff_lzw"

            )



        return output







    def crop_image(
        self,
        image,
        settings
    ):


        mode = settings.get(
            "mode"
        )


        if not mode:

            raise ValueError(
                "Crop mode missing"
            )



        width, height = image.size





        # =====================
        # FIXED CENTER CROP
        # =====================


        if mode == "fixed":


            crop_width = int(
                settings.get(
                    "width"
                )
            )


            crop_height = int(
                settings.get(
                    "height"
                )
            )


            self.validate_crop_size(
                crop_width,
                crop_height,
                width,
                height
            )







        # =====================
        # PERCENTAGE
        # =====================


        elif mode == "percentage":


            value = float(
                settings.get(
                    "value",
                    100
                )
            )


            if value <= 0 or value > 100:

                raise ValueError(
                    "Crop percentage must be between 1 and 100"
                )


            ratio = value / 100


            crop_width = round(
                width * ratio
            )


            crop_height = round(
                height * ratio
            )







        # =====================
        # ASPECT RATIO
        # =====================


        elif mode == "aspect_ratio":


            ratio = settings.get(
                "ratio"
            )


            if not ratio:

                raise ValueError(
                    "Crop ratio missing"
                )


            try:

                ratio_w, ratio_h = map(

                    int,

                    ratio.split(":")

                )


            except Exception:

                raise ValueError(
                    f"Invalid crop ratio: {ratio}"
                )



            if ratio_w <= 0 or ratio_h <= 0:

                raise ValueError(
                    "Invalid crop ratio value"
                )



            target_ratio = ratio_w / ratio_h


            current_ratio = width / height



            if current_ratio > target_ratio:


                crop_width = round(
                    height * target_ratio
                )


                crop_height = height



            else:


                crop_width = width


                crop_height = round(
                    width / target_ratio
                )







        # =====================
        # COORDINATES
        # =====================


        elif mode == "coordinates":


            left = int(
                settings.get(
                    "x",
                    0
                )
            )


            top = int(
                settings.get(
                    "y",
                    0
                )
            )


            crop_width = int(
                settings.get(
                    "width"
                )
            )


            crop_height = int(
                settings.get(
                    "height"
                )
            )



            if left < 0 or top < 0:

                raise ValueError(
                    "Crop coordinates cannot be negative"
                )



            if crop_width <= 0 or crop_height <=0:

                raise ValueError(
                    "Crop dimensions must be positive"
                )



            right = min(
                left + crop_width,
                width
            )


            bottom = min(
                top + crop_height,
                height
            )


            if right <= left or bottom <= top:

                raise ValueError(
                    "Invalid crop area"
                )


            return image.crop(

                (
                    left,
                    top,
                    right,
                    bottom
                )

            )






        else:


            raise ValueError(
                f"Unsupported crop mode: {mode}"
            )





        # =====================
        # CENTER POSITION
        # =====================


        self.validate_crop_size(

            crop_width,

            crop_height,

            width,

            height

        )



        left = (

            width - crop_width

        ) // 2



        top = (

            height - crop_height

        ) // 2



        return image.crop(

            (

                left,

                top,

                left + crop_width,

                top + crop_height

            )

        )







    def validate_crop_size(
        self,
        crop_width,
        crop_height,
        image_width,
        image_height
    ):


        if crop_width <= 0 or crop_height <= 0:

            raise ValueError(
                "Crop dimensions must be positive"
            )



        if crop_width > image_width:

            raise ValueError(
                "Crop width exceeds image width"
            )


        if crop_height > image_height:

            raise ValueError(
                "Crop height exceeds image height"
            )