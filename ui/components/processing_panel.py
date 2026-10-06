from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout
)


from ui.components.processing.resize_section import ResizeSection
from ui.components.processing.crop_section import CropSection
from ui.components.processing.transform_section import TransformSection
from ui.components.processing.compression_section import CompressionSection
from ui.components.processing.dpi_section import DPISection
from ui.components.processing.colorspace_section import ColorSpaceSection
from ui.components.processing.bitdepth_section import BitDepthSection
from ui.components.processing.metadata_section import MetadataSection




class ProcessingPanel(QWidget):


    def __init__(
        self
    ):

        super().__init__()


        self.sections = []


        self.setup_ui()



    def setup_ui(
        self
    ):


        layout = QVBoxLayout()



        self.add_section(
            ResizeSection(),
            layout
        )


        self.add_section(
            CropSection(),
            layout
        )


        self.add_section(
            TransformSection(),
            layout
        )


        self.add_section(
            CompressionSection(),
            layout
        )


        self.add_section(
            DPISection(),
            layout
        )


        self.add_section(
            ColorSpaceSection(),
            layout
        )


        self.add_section(
            BitDepthSection(),
            layout
        )


        self.add_section(
            MetadataSection(),
            layout
        )



        layout.addStretch()



        self.setLayout(
            layout
        )



    def add_section(
        self,
        section,
        layout
    ):


        self.sections.append(
            section
        )


        layout.addWidget(
            section
        )



    def get_operations(
        self
    ):


        operations = []



        for section in self.sections:


            config = section.get_config()



            if config:


                operations.append(
                    config
                )



        return operations