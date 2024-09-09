from fastapi import FastAPI, File, UploadFile, HTTPException
from pypdf import PdfReader
from transformers import pipeline
import io

app = FastAPI()

# In-memory storage for PDF content
pdf_text_storage = {}


@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF file and extract its text content."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File format not supported. Please upload a PDF file.")
    
    # Read the PDF file
    try:
        content = await file.read()
        pdf_reader = PdfReader(io.BytesIO(content))
        extracted_text = ""
        for page in pdf_reader.pages:
            extracted_text += page.extract_text()
        
        # Store the extracted text in memory (using filename as key)
        pdf_text_storage[file.filename] = extracted_text
        
        return {"filename": file.filename, "message": "PDF uploaded and processed successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.get("/ask_question/")
async def ask_question(filename: str, question: str):
    """Answer a question based on the text content of the uploaded PDF."""
    # Check if the PDF content is available
    if filename not in pdf_text_storage:
        raise HTTPException(status_code=404, detail="PDF file not found. Please upload the PDF first.")

    # Get the text content
    pdf_text = pdf_text_storage[filename]

    # Use a question-answering model from transformers
    nlp_pipeline = pipeline("question-answering")
    result = nlp_pipeline(question=question, context=pdf_text)
    
    return {"answer": result['answer']}
