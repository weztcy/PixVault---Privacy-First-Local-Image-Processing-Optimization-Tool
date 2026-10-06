from pathlib import Path

from PIL import Image





class ImageResizer:



    RESAMPLING = {


        "nearest":
            Image.Resampling.NEAREST,


        "bilinear":
            Image.Resampling.BILINEAR,


        "bicubic":
            Image.Resampling.BICUBIC,


        "lanczos":
            Image.Resampling.LANCZOS

    }






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


            resized = self.resize_image(
                image,
                settings
            )


            resized.save(
                output,
                format="TIFF",
                compression="tiff_lzw"
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


        if not method:

            raise ValueError(
                "Resize method missing"
            )



        keep_ratio = settings.get(
            "keep_ratio",
            True
        )



        resampling = self.RESAMPLING.get(

            settings.get(
                "resampling",
                "lanczos"
            ),

            Image.Resampling.LANCZOS

        )



        width, height = image.size





        if method == "exact":


            new_width = settings.get(
                "width"
            )


            new_height = settings.get(
                "height"
            )



            self.validate_size(
                new_width,
                new_height
            )






        elif method == "width":


            new_width = settings.get(
                "value"
            )


            if not new_width:

                raise ValueError(
                    "Resize width missing"
                )


            new_width = int(
                new_width
            )


            if new_width <= 0:

                raise ValueError(
                    "Resize width must be positive"
                )



            if keep_ratio:


                ratio = new_width / width


                new_height = round(
                    height * ratio
                )


            else:

                new_height = height






        elif method == "height":


            new_height = settings.get(
                "value"
            )


            if not new_height:

                raise ValueError(
                    "Resize height missing"
                )


            new_height = int(
                new_height
            )


            if new_height <= 0:

                raise ValueError(
                    "Resize height must be positive"
                )



            if keep_ratio:


                ratio = new_height / height


                new_width = round(
                    width * ratio
                )


            else:

                new_width = width







        elif method == "percentage":


            value = settings.get(
                "value"
            )


            if value is None:

                raise ValueError(
                    "Resize percentage missing"
                )


            value = float(
                value
            )


            if value <= 0:

                raise ValueError(
                    "Resize percentage must be positive"
                )



            ratio = value / 100



            new_width = round(
                width * ratio
            )


            new_height = round(
                height * ratio
            )







        elif method == "longest_side":


            target = settings.get(
                "value"
            )


            if not target:

                raise ValueError(
                    "Longest side value missing"
                )


            target = int(
                target
            )


            ratio = target / max(
                width,
                height
            )


            new_width = round(
                width * ratio
            )


            new_height = round(
                height * ratio
            )







        elif method == "shortest_side":


            target = settings.get(
                "value"
            )


            if not target:

                raise ValueError(
                    "Shortest side value missing"
                )


            target = int(
                target
            )


            ratio = target / min(
                width,
                height
            )


            new_width = round(
                width * ratio
            )


            new_height = round(
                height * ratio
            )






        else:

            raise ValueError(
                f"Unsupported resize method: {method}"
            )



        self.validate_size(
            new_width,
            new_height
        )



        return image.resize(

            (

                int(new_width),

                int(new_height)

            ),

            resampling

        )






    def validate_size(
        self,
        width,
        height
    ):


        if width is None or height is None:

            raise ValueError(
                "Resize dimensions missing"
            )



        width = int(
            width
        )


        height = int(
            height
        )



        if width <= 0 or height <= 0:

            raise ValueError(
                "Resize dimensions must be positive"
            )