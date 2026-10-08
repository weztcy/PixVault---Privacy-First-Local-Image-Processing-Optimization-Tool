from pathlib import Path

from formats import BaseEncoder


class TIFFEncoder(BaseEncoder):
    def save(self, image, output_path, settings):

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        icc = image.info.get("icc_profile")

        image.save(
            output,
            format="TIFF",
            compression=str(settings.get("compression", "LZW")).lower(),
            dpi=(settings.get("dpi", 300), settings.get("dpi", 300)),
            icc_profile=icc,
        )

        return output
