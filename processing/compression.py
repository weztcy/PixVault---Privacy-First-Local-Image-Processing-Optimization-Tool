from pathlib import Path

from PIL import Image





class ImageCompressor:



    def process(
        self,
        source_path,
        output_path,
        settings
    ):


        source = Path(
            source_path
        )


        output = Path(
            output_path
        )


        output.parent.mkdir(
            parents=True,
            exist_ok=True
        )



        with Image.open(source) as image:


            processed = self.compress_image(

                image,

                settings

            )


            processed.save(

                output,

                format="TIFF",

                compression="tiff_lzw"

            )



        return output







    def compress_image(
        self,
        image,
        settings
    ):


        method = settings.get(

            "method",

            "none"

        )





        # =====================
        # NONE
        # =====================


        if method == "none":


            return image.copy()







        # =====================
        # OPTIMIZE
        # =====================


        if method == "optimize":


            optimized = image.copy()


            optimized.info.clear()


            return optimized







        # =====================
        # REMOVE ALPHA
        # =====================


        if method == "remove_alpha":


            return self.remove_alpha(
                image
            )







        raise ValueError(

            f"Unsupported compression method: {method}"

        )







    def remove_alpha(
        self,
        image
    ):


        if image.mode not in [

            "RGBA",

            "LA"

        ]:


            return image.copy()



        background = Image.new(

            "RGB",

            image.size,

            "white"

        )



        alpha = image.getchannel(
            "A"
        )



        background.paste(

            image,

            mask=alpha

        )



        return background