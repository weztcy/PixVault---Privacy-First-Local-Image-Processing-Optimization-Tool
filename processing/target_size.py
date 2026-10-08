"""Target file size optimization engine for PixVault."""

from io import BytesIO


class TargetSizeOptimizer:
    MIN_QUALITY = 5
    MAX_QUALITY = 95

    def to_bytes(self, value, unit="KB"):
        value = float(value)

        if str(unit).upper() == "MB":
            return int(value * 1024 * 1024)

        return int(value * 1024)

    def optimize_jpeg_webp(
        self, image, output_format, target_bytes, base_settings=None
    ):

        settings = dict(base_settings or {})

        low = self.MIN_QUALITY
        high = self.MAX_QUALITY

        best = None
        best_quality = None
        best_diff = None

        while low <= high:
            quality = (low + high) // 2

            buffer = BytesIO()

            save_settings = {
                "format": output_format,
                "quality": quality,
            }

            if output_format == "WEBP":
                save_settings["method"] = settings.get("method", 6)

            image.save(buffer, **save_settings)

            size = buffer.tell()

            diff = abs(size - target_bytes)

            if best_diff is None or diff < best_diff:
                best = buffer.getvalue()
                best_quality = quality
                best_diff = diff

            if size > target_bytes:
                high = quality - 1
            else:
                low = quality + 1

        return best, best_quality

    def optimize_png(self, image, target_bytes):

        best = None

        for level in range(9, -1, -1):
            buffer = BytesIO()

            image.save(
                buffer,
                format="PNG",
                compress_level=level,
                optimize=True,
            )

            if best is None or abs(buffer.tell() - target_bytes) < abs(
                len(best) - target_bytes
            ):
                best = buffer.getvalue()

        return best

    def optimize_tiff(self, image, target_bytes):

        best = None

        for compression in ["deflate", "tiff_lzw"]:
            buffer = BytesIO()

            image.save(
                buffer,
                format="TIFF",
                compression=compression,
            )

            if best is None or abs(buffer.tell() - target_bytes) < abs(
                len(best) - target_bytes
            ):
                best = buffer.getvalue()

        return best
