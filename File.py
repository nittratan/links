import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pdf2image import convert_from_path
from pathlib import Path

# Initialize FastAPI app
app = FastAPI()

# Directory to store the converted images
IMAGE_OUTPUT_DIR = Path("output_images")
IMAGE_OUTPUT_DIR.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)

# Health check route
@app.get("/index")
async def index():
    """
    API health check route.
    """
    logging.info("Health check endpoint hit.")
    return {"message": "API is alive and running!"}

# Route to convert PDF to images
@app.post("/convert-pdf-to-images/")
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

        # Convert PDF to images
        images = convert_from_path(pdf_path, fmt="jpeg")
        logging.info(f"PDF converted to {len(images)} images.")

        image_files = []
        for i, image in enumerate(images):
            output_file = IMAGE_OUTPUT_DIR / f"{pdf_path.stem}_page_{i + 1}.jpeg"
            image.save(output_file, "JPEG")
            image_files.append(str(output_file))
            logging.info(f"Image saved: {output_file}")

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

