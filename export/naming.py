from pathlib import Path

from datetime import datetime



class NamingEngine:



    def generate(
        self,
        source_path,
        output_folder,
        settings
    ):

        source = Path(
            source_path
        )


        output_folder = Path(
            output_folder
        )


        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )


        filename = self.create_filename(
            source,
            settings
        )


        output_path = output_folder / filename


        return self.resolve_collision(
            output_path
        )



    def create_filename(
        self,
        source,
        settings
    ):


        output_format = settings.get(
            "format",
            source.suffix.replace(
                ".",
                ""
            )
        ).lower()



        pattern = settings.get(
            "pattern"
        )


        suffix = settings.get(
            "suffix"
        )



        if pattern:


            filename = pattern.format(

                name=source.stem,

                format=output_format,

                date=datetime.now().strftime(
                    "%Y-%m-%d"
                )

            )


            return (
                filename
                +
                "."
                +
                output_format
            )



        name = source.stem



        if suffix:

            name = (
                name
                +
                "_"
                +
                suffix
            )



        return (
            name
            +
            "."
            +
            output_format
        )



    def resolve_collision(
        self,
        output_path
    ):


        if not output_path.exists():

            return output_path



        counter = 1


        while True:


            new_path = output_path.parent / (

                f"{output_path.stem}_{counter:03d}"

                f"{output_path.suffix}"

            )



            if not new_path.exists():

                return new_path



            counter += 1