from pathlib import Path

from PIL import Image


class ImageResizer:


    RESAMPLING = {

        "nearest": Image.Resampling.NEAREST,

        "bilinear": Image.Resampling.BILINEAR,

        "bicubic": Image.Resampling.BICUBIC,

        "lanczos": Image.Resampling.LANCZOS,

    }



    def process(
        self,
        source_path,
        output_path,
        settings
    ):

        source = Path(source_path)

        output = Path(output_path)


        with Image.open(source) as image:

            resized = self.resize_image(
                image,
                settings
            )


            resized.save(
                output
            )


        return output



    def resize_image(
        self,
        image,
        settings
    ):

        method = settings.get(
            "method"
        )


        keep_ratio = settings.get(
            "keep_aspect_ratio",
            True
        )


        resampling = self.RESAMPLING.get(
            settings.get(
                "resampling",
                "lanczos"
            )
        )


        width, height = image.size



        if method == "exact":

            new_width = settings["width"]

            new_height = settings["height"]



        elif method == "width":

            new_width = settings["value"]

            if keep_ratio:

                ratio = new_width / width

                new_height = int(
                    height * ratio
                )

            else:

                new_height = height



        elif method == "height":

            new_height = settings["value"]

            if keep_ratio:

                ratio = new_height / height

                new_width = int(
                    width * ratio
                )

            else:

                new_width = width



        elif method == "percentage":

            percent = settings["value"] / 100

            new_width = int(
                width * percent
            )

            new_height = int(
                height * percent
            )



        elif method == "longest_side":

            target = settings["value"]

            ratio = target / max(
                width,
                height
            )

            new_width = int(
                width * ratio
            )

            new_height = int(
                height * ratio
            )



        elif method == "shortest_side":

            target = settings["value"]

            ratio = target / min(
                width,
                height
            )

            new_width = int(
                width * ratio
            )

            new_height = int(
                height * ratio
            )



        else:

            return image



        return image.resize(
            (
                new_width,
                new_height
            ),
            resampling
        )