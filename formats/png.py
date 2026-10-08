from pathlib import Path
from formats import BaseEncoder


class PNGEncoder(BaseEncoder):

    def save(self, image, output_path, settings):

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        icc = image.info.get("icc_profile")

        color_type = str(settings.get("color_type","RGBA")).lower()

        if color_type == "gray":
            image = image.convert("L")
        elif color_type == "rgb":
            image = image.convert("RGB")
        else:
            image = image.convert("RGBA")

        if icc:
            image.info["icc_profile"] = icc

        image.save(
            output,
            format="PNG",
            compress_level=int(settings.get("compression",6)),
            icc_profile=icc
        )

        return output
