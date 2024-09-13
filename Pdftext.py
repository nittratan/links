from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

app = FastAPI()

# Load the pre-trained embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from a PDF file."""
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

@app.post("/convert-pdf-to-vector/")
async def convert_pdf_to_vector(file: UploadFile = File(...)):
    # Ensure the uploaded file is a PDF
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")

    # Extract text from the uploaded PDF file
    try:
        text = extract_text_from_pdf(file.file)
        if not text.strip():
            raise HTTPException(status_code=400, detail="PDF is empty or unreadable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {e}")

    # Convert text to vector using the embedding model
    embeddings = model.encode(text)

    return {"vector": embeddings.tolist()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
