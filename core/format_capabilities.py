"""
Format capability matrix.

Used by:
- Format Options UI
- Processing validation
- Export validation

All format names must use uppercase.
"""





FORMAT_CAPABILITIES = {



    "JPEG":
    {

        "resize": True,

        "crop": True,

        "rotate": True,

        "flip": True,


        "compression":
        {

            "modes":
            [

                "quality",

                "target_size"

            ],

            "quality": True,

            "optimize": True,

            "progressive": True,

            "subsampling":
            [

                "4:4:4",

                "4:2:2",

                "4:2:0"

            ]

        },


        "dpi": True,


        "colorspace":
        [

            "sRGB",

            "Adobe RGB",

            "Display P3",

            "CMYK",

            "Grayscale"

        ],


        "bit_depth":
        [

            8

        ],


        "metadata": True

    },









    "PNG":
    {

        "resize": True,

        "crop": True,

        "rotate": True,

        "flip": True,


        "compression":
        {

            "modes":
            [

                "lossless",

                "target_size"

            ],

            "quality": False,

            "compression_level": True,

            "optimize": True,

            "interlace": True

        },


        "dpi": True,


        "colorspace":
        [

            "sRGB",

            "Grayscale"

        ],


        "bit_depth":
        [

            8,

            16

        ],


        "metadata": True

    },









    "WEBP":
    {

        "resize": True,

        "crop": True,

        "rotate": True,

        "flip": True,


        "compression":
        {

            "modes":
            [

                "lossy",

                "lossless"

            ],


            "lossy":
            {

                "quality": True,

                "method": True,

                "alpha_quality": True

            },


            "lossless":
            {

                "quality": False

            }

        },


        "dpi": True,


        "colorspace":
        [

            "sRGB",

            "Grayscale"

        ],


        "bit_depth":
        [

            8

        ],


        "metadata": True

    },









    "AVIF":
    {

        "resize": True,

        "crop": True,

        "rotate": True,

        "flip": True,


        "compression":
        {

            "modes":
            [

                "lossy",

                "lossless"

            ],


            "lossy":
            {

                "quality": True,

                "speed": True,

                "subsampling": True,

                "alpha_quality": True

            },


            "lossless":
            {

                "quality": False

            }

        },


        "dpi": True,


        "colorspace":
        [

            "sRGB",

            "Display P3",

            "Grayscale"

        ],


        "bit_depth":
        [

            8,

            10,

            12

        ],


        "metadata": True

    },









    "GIF":
    {

        "resize": True,

        "crop": True,

        "rotate": True,

        "flip": True,


        "compression":
        {

            "color_count": True,

            "dither": True,

            "optimize": True,

            "quality": False

        },


        "dpi": True,


        "colorspace":
        [

            "sRGB"

        ],


        "bit_depth":
        [

            8

        ],


        "metadata": True

    },









    "BMP":
    {

        "resize": True,

        "crop": True,

        "rotate": True,

        "flip": True,


        "compression":
        {

            "modes":
            [

                "none",

                "rle"

            ],

            "quality": False

        },


        "dpi": True,


        "colorspace":
        [

            "sRGB",

            "Grayscale"

        ],


        "bit_depth":
        [

            8,

            24,

            32

        ],


        "metadata": False

    },









    "TIFF":
    {

        "resize": True,

        "crop": True,

        "rotate": True,

        "flip": True,


        "compression":
        {

            "modes":
            [

                "none",

                "lzw",

                "deflate",

                "jpeg",

                "zstd"

            ],

            "quality": True

        },


        "dpi": True,


        "colorspace":
        [

            "sRGB",

            "Adobe RGB",

            "Display P3",

            "CMYK",

            "Grayscale"

        ],


        "bit_depth":
        [

            8,

            16,

            32

        ],


        "metadata": True

    },









    "HEIC":
    {

        "resize": True,

        "crop": True,

        "rotate": True,

        "flip": True,


        "compression":
        {

            "modes":
            [

                "lossy",

                "lossless"

            ],

            "quality": True

        },


        "dpi": True,


        "colorspace":
        [

            "sRGB",

            "Display P3",

            "Grayscale"

        ],


        "bit_depth":
        [

            8,

            10

        ],


        "metadata": True

    },









    "ICO":
    {

        "resize": True,

        "crop": True,

        "rotate": True,

        "flip": True,


        "compression":
        {

            "quality": False

        },


        "dpi": False,


        "colorspace":
        [

            "sRGB"

        ],


        "bit_depth":
        [

            8,

            32

        ],


        "metadata": False

    },









    "SVG":
    {

        "resize": False,

        "crop": False,

        "rotate": True,

        "flip": True,


        "compression":
        {

            "optimize_path": True,

            "minify": True

        },


        "dpi": False,


        "colorspace":
        [

            "sRGB"

        ],


        "bit_depth":
        [],


        "metadata": True

    }

}









def get_capabilities(
    format_name
):


    return FORMAT_CAPABILITIES.get(

        format_name.upper(),

        {}

    )









def supports(
    format_name,
    feature
):


    capabilities = get_capabilities(

        format_name

    )


    return bool(

        capabilities.get(

            feature,

            False

        )

    )









def get_supported_values(
    format_name,
    feature
):


    capabilities = get_capabilities(

        format_name

    )


    return capabilities.get(

        feature,

        []

    )