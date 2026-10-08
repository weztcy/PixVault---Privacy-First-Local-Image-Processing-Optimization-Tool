# PixVault

PixVault is a privacy-focused Python desktop application for local image processing. It brings image conversion, compression, resizing, cropping, and other image preparation tools into a single workspace, with image processing performed on the user's device without uploading images to internet services or cloud processing platforms.

Built with PySide6 and Pillow, PixVault keeps its image-processing workflow local so users can work with personal or sensitive images without sending them to an external processing provider. Once the application and its dependencies are installed, image processing does not require an internet connection. Dedicated tool pages, background batch processing, configurable exports, and locally stored history support this offline workflow.

## 🖼️ About the Project

PixVault was developed as a local image studio with separate workspaces for common image processing tasks. Its interface organizes conversion, compression, resizing, cropping, transformation, DPI, metadata, color space, and bit depth tools alongside home, history, and privacy pages.

The implementation separates interface components, application services, processing operations, format encoders, export handling, and history storage. Shared services connect the tool pages to the underlying processing pipeline, while reusable option panels organize processing and output settings.

Image operations run through an ordered pipeline before the result is passed to the export layer. This structure provides a foundation for extending individual processors, adding format-specific behavior, and maintaining consistent workflows across the application.

## 🔒 Local Processing and Data Privacy

PixVault processes images locally, without relying on internet connectivity or cloud image-processing services. Source images are read from local files, processing runs on the user's device, and results are saved to the selected output folder. Images do not need to be uploaded to a remote server for conversion, compression, or other image operations.

This local workflow reduces exposure to third-party upload, processing, and retention systems. Users retain control over where source images and exported files are stored, making the application suitable for workflows where keeping image content on the device is a priority.

The privacy-focused workflow includes:
- On-device image processing without cloud processing dependencies
- Offline image operations after the application and required dependencies are installed
- No image uploads required for the processing workflow
- User-selected output folders for generated files
- Locally stored JSON processing history rather than a cloud history service

Local processing does not automatically encrypt files, remove all metadata, or protect against unauthorized access to the device. Processing history can contain source and output paths, and files saved to a cloud-synchronized folder may be uploaded by other software. Users should choose a nonsynchronized local folder when files must remain exclusively on the device and review metadata settings before sharing exported images.

## ✨ Features

Key features and implementations include:
- Privacy-focused, on-device image processing
- Offline image operations without cloud processing or required image uploads
- User-controlled local output storage and local processing history
- Dedicated desktop workspaces for image processing tools
- Image format conversion and format-specific encoder modules
- Image compression processing
- Image resizing and cropping
- Image transformation processing
- DPI adjustment
- Metadata processing
- Color space and bit depth processing
- Configurable processing operations and output settings
- Background batch processing using Qt threads
- Per-file progress updates and success or failure reporting
- Batch cancellation checks between files
- Output folder creation and generated export filenames
- Input validation for single-image processing
- JSON-based processing history
- Reusable interface components and a shared desktop theme
- Separate interface, service, processing, and export layers

## 🔄 Image Conversion and Export

PixVault separates image processing from output encoding. The repository includes encoder modules and corresponding option panels for JPEG, PNG, WebP, AVIF, HEIC, TIFF, GIF, BMP, ICO, and SVG. Actual format availability and supported options depend on the encoder implementation and installed imaging libraries.

The export layer validates the requested output format, creates the destination folder, generates an output filename, and delegates saving to the encoder manager. After saving, it checks that the output file exists and returns its path, format, and file size.

Format-specific settings are organized separately from processing operations, allowing output configuration to remain distinct from changes applied to the image itself.

## 📐 Resizing, Cropping, and Transformations

Dedicated pages and processor modules handle resizing, cropping, and image transformations. These operations share the same pipeline and export infrastructure used by the other tools.

When multiple operations are supplied together, the pipeline applies resizing before cropping, followed by transformations. This defined order determines which version of the image each subsequent operation receives.

## 🗜️ Image Compression

PixVault includes a compression workspace, a compression options panel, and an image compression processor.

Compression processing is handled within the image pipeline, while output encoding is handled by the selected format encoder. The resulting file size and available encoding controls therefore depend on both the processing configuration and the output format.

## 🎨 Color Space and Bit Depth

Color space and bit depth processing have dedicated pages, option panels, and processor modules. Both operations are integrated into the shared processing pipeline before DPI and metadata processing.

The repository also defines a location for ICC profiles used by professional color conversion. Genuine Adobe RGB, Display P3, FOGRA39, and grayscale profile files must be supplied for conversions that require them; the corresponding text files in the repository are placement instructions.

## 🏷️ DPI and Metadata

PixVault provides separate workspaces for DPI and metadata processing. Each tool has its own configuration panel and processor, keeping these settings distinct from geometric image operations and format encoding.

DPI processing runs near the end of the pipeline, followed by metadata processing. The resulting image is then passed to the export layer for saving in the selected format.

## ⚙️ Processing Pipeline

The central image pipeline loads the source image, validates the output configuration, sorts the requested operations, and passes the image through the corresponding processors.

Operations follow this sequence:
- Resize
- Crop
- Transform
- Compression
- Bit depth
- Color space
- DPI
- Metadata

Each processor receives the image produced by the preceding operation. The pipeline then exports the result and records a successful processing entry in history.

The single-image service also checks that an input path refers to an existing, nonempty file that Pillow can verify before starting processing.

## 📚 Batch Processing and Progress

Batch processing runs through a Qt worker thread, moving the image-processing workload away from the main interface thread. Files are processed sequentially within each batch.

The worker reports progress and collects successful output paths, failed files with error messages, the total file count, and the processed count. A failure affecting one file is captured so that processing can continue with subsequent files.

Cancellation is checked before starting the next file. A cancellation request does not interrupt an individual image operation already in progress.

## 🗂️ Processing History

PixVault includes a dedicated history layer and a history page for processing records. History is stored locally in JSON.

Records associate source files and output files with the selected format, applied operations, processing status, timestamps, and error information where applicable. This provides a local record of processing activity alongside the image tools.

## 🖥️ Desktop Interface and Architecture

The interface uses PySide6 with a stacked workspace for switching between pages inside the main window. Shared image, batch, and history services are supplied to the workspace rather than recreated independently for every page.

Reusable components organize image importing, previews, image information, output selection, encoder settings, processing options, and export progress. A shared dark navy and emerald theme provides consistent styling across the application.

The repository separates application startup, interface code, services, core processing, individual operations, format encoders, export utilities, and history management.

## 🛠️ Technologies

The main technologies and libraries listed in this project are:
- Python
- PySide6
- Pillow
- pillow-heif
- pillow-avif-plugin
- NumPy
- rawpy
- svgwrite
- tifffile
- JSON for local history storage

## 🎯 Project Objectives

This project was developed to:
- Keep image processing on the user's device without requiring image uploads to external services
- Reduce reliance on third-party cloud platforms when working with personal or sensitive images
- Enable offline image processing after installation
- Give users control over local image storage and exported results
- Provide a desktop workspace for local image processing
- Bring common image preparation tools into one application
- Support configurable image operations and output encoding
- Organize multi-file processing with progress and result reporting
- Maintain local records of image processing activity
- Separate interface behavior from processing and export logic
- Establish a modular foundation for further image tools and format integrations

## 📜 License

This project is maintained for portfolio, reference, and development purposes.

---

**PixVault — Private Offline Image Processing**