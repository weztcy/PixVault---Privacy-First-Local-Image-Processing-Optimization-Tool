from io import BytesIO


class ImageCompressor:
    PRIORITY_STEPS = {"size": 10, "balanced": 5, "quality": 2}

    def process(self, image, settings):

        mode = settings.get("mode", "quality")

        if mode == "quality":
            return self.quality_compression(image, settings)

        elif mode == "target_size":
            return self.target_size_compression(image, settings)

        else:
            raise ValueError(f"Unsupported compression mode: {mode}")

    def quality_compression(self, image, settings):

        quality = settings.get("quality", 85)

        optimize = settings.get("optimize", True)

        if quality < 1 or quality > 100:
            raise ValueError("Quality must be between 1 and 100")

        result = image.copy()

        result.info["compression"] = {
            "quality": int(quality),
            "optimize": bool(optimize),
        }

        return result

    def target_size_compression(self, image, settings):

        target_size = settings.get("size")

        unit = settings.get("unit", "KB")

        priority = settings.get("priority", "balanced")

        if target_size is None:
            raise ValueError("Target size missing")

        target_bytes = self.convert_size(target_size, unit)

        if target_bytes <= 0:
            raise ValueError("Target size must be positive")

        result = image.copy()

        result.info["compression"] = {"target_size": target_bytes, "priority": priority}

        return result

    def compress_to_target_size(
        self, image, output_format, target_bytes, priority="balanced"
    ):

        quality = 95

        step = self.PRIORITY_STEPS.get(priority, 5)

        while quality > 5:
            buffer = BytesIO()

            save_options = {"format": output_format, "quality": quality}

            image.save(buffer, **save_options)

            current_size = buffer.tell()

            if current_size <= target_bytes:
                return buffer.getvalue(), quality

            quality -= step

        return buffer.getvalue(), quality

    def convert_size(self, value, unit):

        value = float(value)

        unit = unit.upper()

        if unit == "KB":
            return int(value * 1024)

        if unit == "MB":
            return int(value * 1024 * 1024)

        raise ValueError(f"Unsupported size unit: {unit}")
