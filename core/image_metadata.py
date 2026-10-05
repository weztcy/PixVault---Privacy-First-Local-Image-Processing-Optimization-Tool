from pathlib import Path

from PIL import Image


class ImageData:

    def __init__(self):

        self.path = None
        self.filename = None
        self.extension = None
        self.format = None
        self.size_bytes = 0
        self.width = 0
        self.height = 0
        self.mode = None
        self.has_metadata = False
        self.thumbnail = None



class ImageMetadata:


    def read(self, file_path):

        path = Path(file_path)

        data = ImageData()


        data.path = str(path)

        data.filename = path.name

        data.extension = path.suffix.lower()

        data.size_bytes = path.stat().st_size


        try:

            with Image.open(path) as image:

                data.format = image.format

                data.width = image.width

                data.height = image.height

                data.mode = image.mode


                if image.info:

                    data.has_metadata = True


        except Exception:

            data.format = "Unknown"


        return data