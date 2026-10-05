from pathlib import Path


from formats.encoder import EncoderManager

from export.naming import NamingEngine




class Exporter:



    def __init__(self):

        self.encoder = EncoderManager()

        self.naming = NamingEngine()



    def export(
        self,
        image,
        source_path,
        output_folder,
        settings
    ):


        output_path = self.naming.generate(
            source_path,
            output_folder,
            settings
        )


        self.encoder.save(
            image,
            output_path,
            settings
        )


        return {

            "path": output_path,

            "format": settings.get(
                "format"
            ),

            "size": output_path.stat().st_size

        }