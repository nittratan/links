from fastapi import FastAPI, HTTPException
import requests
from PyPDF2 import PdfReader
from io import BytesIO

app = FastAPI()

# Example list of URLs
policy_URL = [
    "https://example.com/document1.pdf",
    "https://example.com/document2.pdf"
]

@app.get("/pdfs_from_urls/")
async def read_pdfs_from_urls():
    """Read PDFs from a static list of URLs and extract their text content."""
    pdf_texts = []

    for url in policy_URL:
        if not url.endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"URL {url} does not point to a PDF file.")

        # Read the PDF file from the URL
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to download PDF from {url}")

        try:
            # Read the PDF content
            pdf = PdfReader(BytesIO(response.content))
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
            pdf_texts.append(text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing PDF from {url}: {str(e)}")

    return {"message": "PDFs processed successfully!", "pdf_texts": pdf_texts}
