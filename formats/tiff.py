from pathlib import Path

from formats import BaseEncoder


class TIFFEncoder(BaseEncoder):
    def save(self, image, output_path, settings):

        output = Path(output_path)

        output.parent.mkdir(parents=True, exist_ok=True)

        compression = str(settings.get("compression", "LZW")).upper()

        bit_depth = int(settings.get("bit_depth", 8))

        color = str(settings.get("color", "RGB")).upper()

        dpi = float(settings.get("dpi", 300))

        quality = int(settings.get("quality", 85))

        image = self.prepare_image(image, color, bit_depth)

        save_settings = {
            "format": "TIFF",
            "compression": self.get_compression(compression),
            "dpi": (dpi, dpi),
        }

        if compression == "JPEG":
            save_settings["quality"] = quality

        icc_profile = image.info.get("icc_profile")

        if icc_profile:
            save_settings["icc_profile"] = icc_profile

        image.save(output, **save_settings)

        return output

    def get_compression(self, compression):

        mapping = {
            "NONE": None,
            "LZW": "tiff_lzw",
            "DEFLATE": "tiff_adobe_deflate",
            "PACKBITS": "packbits",
            "JPEG": "jpeg",
        }

        return mapping.get(compression, "tiff_lzw")

    def prepare_image(self, image, color, bit_depth):

        if color == "RGBA":
            image = image.convert("RGBA")

        elif color == "RGB":
            image = image.convert("RGB")

        elif color in ["GRAY", "GRAYSCALE"]:
            image = image.convert("L")

        elif color == "CMYK":
            image = image.convert("CMYK")

        else:
            raise ValueError(f"Unsupported TIFF color mode: {color}")

        if bit_depth == 8:
            return image

        if bit_depth == 16:
            if image.mode == "L":
                return image.convert("I;16")

            raise ValueError("TIFF 16-bit only supported for grayscale")

        if bit_depth == 32:
            raise ValueError("TIFF 32-bit output is not supported by this encoder")

        raise ValueError(f"Unsupported TIFF bit depth: {bit_depth}")
