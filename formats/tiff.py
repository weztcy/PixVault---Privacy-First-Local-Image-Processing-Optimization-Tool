from pathlib import Path

from PIL import Image

from formats import BaseEncoder



class TIFFEncoder(BaseEncoder):


    def save(
        self,
        image,
        output_path,
        settings
    ):

        output = Path(output_path)


        compression = settings.get(
            "compression",
            "tiff_lzw"
        )


        dpi = settings.get(
            "dpi",
            None
        )


        save_settings = {

            "format": "TIFF",

            "compression": compression

        }


        if dpi:

            save_settings["dpi"] = dpi


        image.save(
            output,
            **save_settings
        )


        return output