from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from pymongo import MongoClient
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI()

# MongoDB connection
client = MongoClient("your_mongodb_url")
db = client["starts-sit"]
user_collection = db["test_user_collection"]
roles_mapping_collection = db["test_roles_doc_mapping"]
sessions_collection = db["test_sessions_collecti"]

# Security setup
SECRET_KEY = "your_secret_key"  # Replace with a secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Helper function to hash password
def get_password_hash(password):
    return pwd_context.hash(password)

# Helper function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Helper function to create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# User schema
class User(BaseModel):
    domain_id: str
    role: str
    password: str

# Signup route
@app.post("/signup")
async def signup(user: User):
    # Check if user already exists
    if user_collection.find_one({"domain_id": user.domain_id}):
        raise HTTPException(status_code=400, detail="Domain ID already registered")

    # Hash password and save user
    hashed_password = get_password_hash(user.password)
    user_collection.insert_one({"domain_id": user.domain_id, "role": user.role, "password": hashed_password})
    return {"message": "User created successfully"}

# Login route
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_collection.find_one({"domain_id": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["domain_id"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Protected route example
@app.get("/get-user-info")
async def get_user_info(token: str = Depends(oauth2_scheme)):
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        domain_id: str = payload.get("sub")
        if domain_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    # Fetch user and related data
    user = user_collection.find_one({"domain_id": domain_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch documents from test_roles_doc_mapping
    role_docs = roles_mapping_collection.find_one({"role": user['role']})
    documents = role_docs["documents"] if role_docs else []

    # Fetch sessions from test_sessions_collecti
    session = sessions_collection.find_one({"domain_id": domain_id})
    sessions = session.get("sessions", []) if session else []

    # Response
    response = {
        "domain_id": domain_id,
        "role": user['role'],
        "documents": documents,
        "sessions": sessions,
    }

    return response

# Health check route
@app.get("/ping")
async def ping():
    try:
        db.command("ping")
        return {"message": "Database is connected!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
