from PIL import Image


class BitDepthProcessor:
    def process(self, image, settings):

        value = settings.get("value", settings.get("bit_depth", 8))

        try:
            bit_depth = int(value)

        except Exception:
            raise ValueError("Invalid bit depth value")

        return self.convert_bitdepth(image, bit_depth)

    def convert_bitdepth(self, image, bit_depth):

        if bit_depth == 8:
            return self.convert_8bit(image)

        if bit_depth == 16:
            return self.convert_16bit(image)

        if bit_depth == 32:
            return self.convert_32bit(image)

        raise ValueError(f"Unsupported bit depth: {bit_depth}")

    def convert_8bit(self, image):

        mode = image.mode

        if mode in ["RGB", "RGBA", "L"]:
            return image

        if "A" in mode:
            return image.convert("RGBA")

        return image.convert("RGB")

    def convert_16bit(self, image):

        mode = image.mode

        # grayscale

        if mode == "L":
            return image.convert("I;16")

        # RGB

        if mode == "RGB":
            channels = image.split()

            converted = [channel.convert("I;16") for channel in channels]

            return Image.merge("RGB", converted)

        if mode == "RGBA":
            return image.convert("RGBA")

        return image.convert("I;16")

    def convert_32bit(self, image):

        # Pillow hanya memiliki float mode F

        # terutama untuk scientific grayscale

        if image.mode == "F":
            return image

        return image.convert("F")
