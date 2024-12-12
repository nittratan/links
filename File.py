import logging
from fastapi import APIRouter, File, UploadFile, HTTPException
from pathlib import Path
from utils.file_utils.py import extract_images

router = APIRouter()

# Directory to store the converted images
IMAGE_OUTPUT_DIR = Path("output_images")

@router.get("/index")
async def index():
    """
    API health check route.
    """
    logging.info("Health check endpoint hit.")
    return {"message": "API is alive and running!"}

@router.post("/convert-pdf-to-images/")
async def convert_pdf_to_images(file: UploadFile = File(...)):
    """
    Upload a PDF file and convert its pages to images.
    """
    try:
        # Validate file type
        if not file.filename.endswith(".pdf"):
            logging.warning("Uploaded file is not a PDF.")
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")

        # Save the uploaded PDF to the server
        pdf_path = Path(file.filename)
        with pdf_path.open("wb") as f:
            f.write(await file.read())
        logging.info(f"Uploaded file saved as: {pdf_path}")

        # Extract images from the PDF
        image_files = extract_images(pdf_path, IMAGE_OUTPUT_DIR)

        # Cleanup uploaded PDF
        pdf_path.unlink()
        logging.info(f"Uploaded PDF deleted: {pdf_path}")

        return {"message": "PDF converted successfully!", "images": image_files}

    except HTTPException as e:
        logging.error(f"HTTPException: {e.detail}")
        raise e

    except Exception as e:
        logging.exception("An error occurred while processing the PDF.")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")
