from pathlib import Path

from PIL import Image



class ImageCropper:


    def process(
        self,
        source_path,
        output_path,
        settings
    ):

        source = Path(source_path)

        output = Path(output_path)


        with Image.open(source) as image:

            cropped = self.crop_image(
                image,
                settings
            )


            cropped.save(
                output
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


        width, height = image.size



        if mode == "fixed":

            crop_width = settings["width"]

            crop_height = settings["height"]


            left = (
                width - crop_width
            ) // 2


            top = (
                height - crop_height
            ) // 2


            right = left + crop_width

            bottom = top + crop_height



        elif mode == "percentage":

            percent = (
                settings["value"]
                /
                100
            )


            crop_width = int(
                width * percent
            )

            crop_height = int(
                height * percent
            )


            left = (
                width - crop_width
            ) // 2


            top = (
                height - crop_height
            ) // 2


            right = left + crop_width

            bottom = top + crop_height



        elif mode == "coordinates":

            left = settings["x"]

            top = settings["y"]

            right = (
                left +
                settings["width"]
            )

            bottom = (
                top +
                settings["height"]
            )



        elif mode == "aspect_ratio":

            target_ratio = (
                settings["width"]
                /
                settings["height"]
            )


            current_ratio = (
                width
                /
                height
            )


            if current_ratio > target_ratio:

                crop_width = int(
                    height * target_ratio
                )

                crop_height = height


            else:

                crop_width = width

                crop_height = int(
                    width / target_ratio
                )


            left = (
                width - crop_width
            ) // 2


            top = (
                height - crop_height
            ) // 2


            right = left + crop_width

            bottom = top + crop_height



        else:

            return image



        return image.crop(
            (
                left,
                top,
                right,
                bottom
            )
        )