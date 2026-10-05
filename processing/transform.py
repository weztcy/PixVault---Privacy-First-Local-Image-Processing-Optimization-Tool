from pathlib import Path

from PIL import Image



class ImageTransformer:


    def process(
        self,
        source_path,
        output_path,
        settings
    ):

        source = Path(source_path)

        output = Path(output_path)


        with Image.open(source) as image:

            transformed = self.apply_transform(
                image,
                settings
            )


            transformed.save(
                output
            )


        return output



    def apply_transform(
        self,
        image,
        settings
    ):

        operation = settings.get(
            "operation"
        )


        if operation == "rotate":

            angle = settings.get(
                "angle",
                0
            )


            return image.rotate(
                angle,
                expand=True
            )



        elif operation == "flip":

            direction = settings.get(
                "direction"
            )


            if direction == "horizontal":

                return image.transpose(
                    Image.Transpose.FLIP_LEFT_RIGHT
                )


            elif direction == "vertical":

                return image.transpose(
                    Image.Transpose.FLIP_TOP_BOTTOM
                )


            elif direction == "both":

                flipped = image.transpose(
                    Image.Transpose.FLIP_LEFT_RIGHT
                )


                return flipped.transpose(
                    Image.Transpose.FLIP_TOP_BOTTOM
                )



        return image