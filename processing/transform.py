from pathlib import Path

from PIL import Image





class ImageTransformer:



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


            transformed = self.apply_transform(

                image,

                settings

            )


            transformed.save(

                output,

                format="TIFF",

                compression="tiff_lzw"

            )



        return output







    def apply_transform(
        self,
        image,
        settings
    ):


        rotation = settings.get(
            "rotation",
            "none"
        )


        flip = settings.get(
            "flip",
            "none"
        )



        image = self.apply_rotation(

            image,

            rotation

        )



        image = self.apply_flip(

            image,

            flip

        )



        return image







    def apply_rotation(
        self,
        image,
        rotation
    ):


        if rotation in [
            None,
            "none"
        ]:

            return image



        try:

            angle = int(
                rotation
            )


        except Exception:

            raise ValueError(

                f"Invalid rotation angle: {rotation}"

            )



        if angle not in [
            90,
            180,
            270,
            -90,
            -180,
            -270
        ]:

            raise ValueError(

                "Rotation must be 90,180,270"

            )



        return image.rotate(

            -angle,

            expand=True

        )









    def apply_flip(
        self,
        image,
        flip
    ):


        if flip in [
            None,
            "none"
        ]:

            return image





        if flip == "horizontal":


            return image.transpose(

                Image.Transpose.FLIP_LEFT_RIGHT

            )






        if flip == "vertical":


            return image.transpose(

                Image.Transpose.FLIP_TOP_BOTTOM

            )






        if flip == "both":


            image = image.transpose(

                Image.Transpose.FLIP_LEFT_RIGHT

            )


            return image.transpose(

                Image.Transpose.FLIP_TOP_BOTTOM

            )






        raise ValueError(

            f"Unsupported flip mode: {flip}"

        )