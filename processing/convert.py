from pathlib import Path

from PIL import Image


class ImageConverter:

    def __init__(self):
        pass


    def convert(
        self,
        source_path,
        output_path,
        output_format
    ):

        source = Path(source_path)

        output = Path(output_path)


        with Image.open(source) as image:


            converted = self.prepare_image(
                image,
                output_format
            )


            converted.save(
                output,
                format=output_format
            )


        return output



    def prepare_image(
        self,
        image,
        output_format
    ):

        output_format = output_format.upper()


        # JPEG tidak mendukung alpha channel
        if output_format in [
            "JPEG",
            "JPG"
        ]:

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
                    mask=image.getchannel("A")
                )

                return background


            elif image.mode != "RGB":

                return image.convert(
                    "RGB"
                )


        return image



    def get_output_extension(
        self,
        output_format
    ):

        mapping = {

            "JPEG": ".jpg",
            "JPG": ".jpg",
            "PNG": ".png",
            "WEBP": ".webp",
            "AVIF": ".avif",
            "GIF": ".gif",
            "BMP": ".bmp",
            "TIFF": ".tiff",
            "TIF": ".tiff",
            "ICO": ".ico",

        }


        return mapping.get(
            output_format.upper()
        )