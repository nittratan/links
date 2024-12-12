import logging
from pathlib import Path
from pdf2image import convert_from_path

# Configure logging for utils
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)

def extract_images(pdf_path: Path, output_dir: Path) -> list:
    """
    Extracts images from a PDF file and saves them to the specified output directory.

    :param pdf_path: Path to the PDF file
    :param output_dir: Directory where images will be saved
    :return: List of paths to the saved images
    """
    try:
        # Ensure the output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)

        # Convert PDF to images
        images = convert_from_path(pdf_path, fmt="jpeg")
        logging.info(f"Extracting {len(images)} images from {pdf_path}")

        image_files = []
        for i, image in enumerate(images):
            output_file = output_dir / f"{pdf_path.stem}_page_{i + 1}.jpeg"
            image.save(output_file, "JPEG")
            image_files.append(str(output_file))
            logging.info(f"Image saved: {output_file}")

        return image_files

    except Exception as e:
        logging.exception(f"Error while extracting images from PDF: {e}")
        raise
