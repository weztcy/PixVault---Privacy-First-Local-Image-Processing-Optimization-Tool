from abc import ABC, abstractmethod




class BaseEncoder(
    ABC
):


    """
    Base interface
    for all PixVault encoders.
    """



    @abstractmethod
    def save(
        self,
        image,
        output_path,
        settings
    ):

        """
        Save processed image.

        Parameters:

        image:
            PIL.Image object


        output_path:
            Destination file path


        settings:
            Encoder configuration dictionary

        """

        raise NotImplementedError