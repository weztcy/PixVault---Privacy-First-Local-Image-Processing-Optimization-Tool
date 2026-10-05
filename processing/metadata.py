from pathlib import Path

from PIL import Image



class MetadataProcessor:



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
            "all"
        )


        with Image.open(source) as image:

            cleaned = self.remove_metadata(
                image,
                mode,
                settings
            )


            save_kwargs = {}


            if output.suffix.lower() in [
                ".jpg",
                ".jpeg"
            ]:

                save_kwargs["exif"] = b""


            cleaned.save(
                output,
                **save_kwargs
            )


        return output



    def remove_metadata(
        self,
        image,
        mode,
        settings
    ):

        clean_image = Image.new(
            image.mode,
            image.size
        )


        clean_image.putdata(
            list(
                image.getdata()
            )
        )


        return clean_image



    def get_metadata(
        self,
        image_path
    ):

        with Image.open(image_path) as image:

            return image.getexif()