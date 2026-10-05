from pathlib import Path

from PIL import Image



class ImageCompressor:



    def process(
        self,
        source_path,
        output_path,
        settings
    ):

        source = Path(source_path)

        output = Path(output_path)


        mode = settings.get(
            "mode",
            "quality"
        )


        with Image.open(source) as image:

            self.compress_image(
                image,
                output,
                settings,
                mode
            )


        return output



    def compress_image(
        self,
        image,
        output,
        settings,
        mode
    ):


        if mode == "quality":

            quality = settings.get(
                "quality",
                85
            )


            image.save(
                output,
                quality=quality,
                optimize=True
            )



        elif mode == "target_size":

            self.compress_target_size(
                image,
                output,
                settings
            )



    def compress_target_size(
        self,
        image,
        output,
        settings
    ):

        target_kb = settings.get(
            "size_kb",
            500
        )


        priority = settings.get(
            "priority",
            "balanced"
        )


        quality = 90


        if priority == "prioritize_size":

            quality = 50


        elif priority == "balanced":

            quality = 70


        elif priority == "prioritize_quality":

            quality = 85



        while quality > 10:

            image.save(
                output,
                quality=quality,
                optimize=True
            )


            size_kb = (
                output.stat().st_size
                /
                1024
            )


            if size_kb <= target_kb:

                break


            quality -= 5