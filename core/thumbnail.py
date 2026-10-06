from pathlib import Path

from PIL import Image


class ThumbnailGenerator:
    def __init__(self, size=(120, 120)):

        self.size = size

    def generate(self, image_path, output_path=None):

        image_path = Path(image_path)

        with Image.open(image_path) as image:
            image.thumbnail(self.size)

            if output_path:
                image.save(output_path)

                return output_path

            return image.copy()
