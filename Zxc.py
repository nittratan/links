from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List, Dict

# Initialize the FastAPI app
app = FastAPI()

# MongoDB connection
client = MongoClient("your_mongodb_url")
db = client["starts-sit"]

# Collections
user_collection = db["test_user_collection"]
roles_mapping_collection = db["test_roles_doc_mapping"]
sessions_collection = db["test_sessions_collecti"]

# Payload schema
class Payload(BaseModel):
    domain_id: str
    role: str

# Health check route
@app.get("/ping")
async def ping():
    try:
        # Attempt to get a document to check if the DB is connected
        db.command("ping")
        return {"message": "Database is connected!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Main route to get user information
@app.post("/get-user-info")
async def get_user_info(payload: Payload):
    # Extract domain_id and role from the payload
    domain_id = payload.domain_id
    role = payload.role

    # Check if domain_id and role exist in test_user_collection
    user = user_collection.find_one({"domain_id": domain_id, "role": role})

    if not user:
        raise HTTPException(status_code=404, detail="User with given domain_id and role not found")

    # Fetch documents from test_roles_doc_mapping
    role_docs = roles_mapping_collection.find_one({"role": role})
    documents = role_docs["documents"] if role_docs else []

    # Fetch session from test_sessions_collecti
    session = sessions_collection.find_one({"domain_id": domain_id})
    sessions = session.get("sessions", []) if session else []

    # Response
    response = {
        "domain_id": domain_id,
        "role": role,
        "documents": documents,
        "sessions": sessions,
    }

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
