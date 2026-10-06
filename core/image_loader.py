from pathlib import Path

from core.image_metadata import ImageMetadata
from core.thumbnail import ThumbnailGenerator

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".avif",
    ".gif",
    ".svg",
    ".bmp",
    ".tiff",
    ".tif",
    ".heic",
    ".heif",
    ".ico",
    ".raw",
}


class ImageLoader:
    def __init__(self):

        self.metadata_reader = ImageMetadata()

        self.thumbnail_generator = ThumbnailGenerator()

    def load_file(self, file_path):

        path = Path(file_path)

        if not self.is_supported(path):
            return []

        image = self.metadata_reader.read(path)

        image = self.attach_thumbnail(image)

        return [image]

    def load_files(self, files):

        images = []

        for file in files:
            images.extend(self.load_file(file))

        return images

    def load_folder(self, folder_path, include_subfolders=False):

        folder = Path(folder_path)

        images = []

        if not folder.exists():
            return images

        if include_subfolders:
            files = folder.rglob("*")

        else:
            files = folder.glob("*")

        for file in files:
            if self.is_supported(file):
                image = self.metadata_reader.read(file)

                image = self.attach_thumbnail(image)

                images.append(image)

        return images

    def attach_thumbnail(self, image):

        try:
            image.thumbnail = self.thumbnail_generator.generate(image.path)

        except Exception:
            image.thumbnail = None

        return image

    def is_supported(self, path):

        return path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
