from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from qdrant_client import QdrantClient

app = FastAPI()

# Initialize Qdrant client
qdrant_client = QdrantClient(host="localhost", port=6333)  # Adjust host/port if needed

# Set your OpenAI API key
openai.api_key = "your_openai_api_key"

# Define the request schema
class QueryRequest(BaseModel):
    query: str
    document_id: str

# Fetch PDF text from VectorDB (Qdrant)
def fetch_pdf_text_from_qdrant(document_id: str) -> str:
    search_result = qdrant_client.search(
        collection_name="pdf_documents",  # Use the name of your Qdrant collection
        query_vector=[1.0],  # Example, your query vector, replace this with appropriate search logic
        filter={
            "must": [
                {
                    "key": "document_id",
                    "match": {"value": document_id}
                }
            ]
        },
        limit=1
    )
    if search_result:
        return search_result[0].payload.get("text", "")
    return None

# Call OpenAI with the fetched text
def generate_openai_response(query: str, document_text: str) -> str:
    response = openai.Completion.create(
        model="gpt-3.5-turbo",  # Adjust to the model you want to use
        prompt=f"Document: {document_text}\n\nUser query: {query}",
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# FastAPI endpoint to handle the query
@app.post("/query")
async def query_pdf(request: QueryRequest):
    document_text = fetch_pdf_text_from_qdrant(request.document_id)
    if not document_text:
        raise HTTPException(status_code=404, detail="Document not found")

    openai_response = generate_openai_response(request.query, document_text)
    return {"answer": openai_response}

# To run the app
# uvicorn script_name:app --reload
