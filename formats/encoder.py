from formats import BaseEncoder

from formats.jpeg import JPEGEncoder
from formats.png import PNGEncoder
from formats.webp import WEBPEncoder
from formats.avif import AVIFEncoder
from formats.gif import GIFEncoder
from formats.bmp import BMPEncoder
from formats.tiff import TIFFEncoder
from formats.heic import HEICEncoder
from formats.ico import ICOEncoder



class EncoderManager:


    def __init__(self):

        self.encoders = {

            "JPG": JPEGEncoder(),
            "JPEG": JPEGEncoder(),

            "PNG": PNGEncoder(),

            "WEBP": WEBPEncoder(),

            "AVIF": AVIFEncoder(),

            "GIF": GIFEncoder(),

            "BMP": BMPEncoder(),

            "TIFF": TIFFEncoder(),
            "TIF": TIFFEncoder(),

            "HEIC": HEICEncoder(),

            "ICO": ICOEncoder(),

        }



    def save(
        self,
        image,
        output_path,
        settings
    ):


        format_name = settings.get(
            "format"
        )


        format_name = format_name.upper()


        encoder = self.encoders.get(
            format_name
        )


        if not encoder:

            raise ValueError(
                f"Unsupported format: {format_name}"
            )


        return encoder.save(
            image,
            output_path,
            settings
        )