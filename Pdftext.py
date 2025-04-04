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



Sure bhai! Yahaan ek solid aur professional answer hai jo tu apne manager ko bhej sakta hai:


---

How the AWS Cloud Practitioner Certification Will Help the Organization and Our Project:

Pursuing the AWS Certified Cloud Practitioner certification will equip me with a strong foundational understanding of AWS cloud services, architecture, and best practices. This knowledge will directly benefit both the organization and our ongoing projects in the following ways:

1. Better Cloud Cost Optimization: With a solid grasp of AWS billing, pricing models, and cost control mechanisms, I’ll be able to suggest ways to optimize resource usage and reduce unnecessary cloud expenditures—leading to direct cost savings for the organization.


2. Improved Architecture Decisions: Understanding AWS core services like EC2, S3, RDS, and networking components will help me contribute to more reliable, secure, and scalable architectural designs.


3. Faster Issue Resolution: A foundational knowledge of AWS helps in faster debugging and troubleshooting of cloud-related issues, improving the turnaround time for incidents and support.


4. Alignment with Industry Standards: AWS certification ensures I’m aligned with best practices and security guidelines that are critical in industries like healthcare, where compliance and data integrity are key.


5. Cross-team Collaboration: The certification will help me communicate more effectively with DevOps, Cloud, and Infrastructure teams, speeding up development and deployment cycles.


6. Foundation for Advanced Certifications: This certification sets the stage for advanced AWS certifications (like Solutions Architect or DevOps Engineer), which can bring even greater value to our cloud initiatives in the long run.



By investing in this certification, the organization is not only upskilling an internal resource but also strengthening its cloud capabilities to stay ahead in a competitive, tech-driven landscape.


---

Bhai agar chahe toh isme thoda customize bhi kar denge, project-specific points add karke. Let me know.

