from datetime import datetime
from pathlib import Path


class NamingEngine:
    FORMAT_EXTENSION = {
        "JPEG": "jpg",
        "PNG": "png",
        "WEBP": "webp",
        "AVIF": "avif",
        "GIF": "gif",
        "BMP": "bmp",
        "TIFF": "tiff",
        "HEIC": "heic",
        "ICO": "ico",
        "SVG": "svg",
    }

    def generate(self, source_path, output_folder, settings):

        source = Path(source_path)

        output_folder = Path(output_folder)

        output_folder.mkdir(parents=True, exist_ok=True)

        filename = self.create_filename(source, settings)

        return self.resolve_collision(output_folder / filename)

    def normalize_extension(self, format_name):

        if not format_name:
            return None

        format_name = str(format_name).upper().strip().lstrip(".")

        extension = self.FORMAT_EXTENSION.get(format_name)

        if extension:
            return extension

        return format_name.lower()

    def create_filename(self, source, settings):

        extension = self.normalize_extension(settings.get("format"))

        if not extension:
            extension = source.suffix.replace(".", "")

        pattern = settings.get("pattern")

        suffix = settings.get("suffix")

        if pattern:
            try:
                filename = pattern.format(
                    name=source.stem,
                    format=extension,
                    date=datetime.now().strftime("%Y-%m-%d"),
                )

            except KeyError as error:
                raise ValueError(f"Invalid filename pattern: {error}")

            if not filename.lower().endswith(f".{extension}"):
                filename += f".{extension}"

            return filename

        name = source.stem

        if suffix:
            suffix = self.sanitize_name(suffix)

            if suffix:
                name += "_" + suffix

        return name + "." + extension

    def sanitize_name(self, value):

        value = str(value)

        forbidden = ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]

        for char in forbidden:
            value = value.replace(char, "_")

        return value.strip()

    def resolve_collision(self, output_path):

        if not output_path.exists():
            return output_path

        counter = 1

        while True:
            new_path = output_path.parent / (
                f"{output_path.stem}_{counter:03d}{output_path.suffix}"
            )

            if not new_path.exists():
                return new_path

            counter += 1
