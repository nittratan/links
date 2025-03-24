from fastapi import FastAPI, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr
from typing import List
from bson import ObjectId

app = FastAPI()

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "user_db"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]
users_collection = db["users"]

# Pydantic Models
class User(BaseModel):
    name: str
    email: EmailStr
    age: int

class UserResponse(User):
    id: str

# Helper function to format MongoDB document
def user_serializer(user) -> dict:
    return {"id": str(user["_id"]), "name": user["name"], "email": user["email"], "age": user["age"]}

# Routes

@app.post("/users/", response_model=UserResponse)
async def create_user(user: User):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = await users_collection.insert_one(user.dict())
    created_user = await users_collection.find_one({"_id": new_user.inserted_id})
    return user_serializer(created_user)

@app.get("/users/", response_model=List[UserResponse])
async def get_users():
    users = await users_collection.find().to_list(100)
    return [user_serializer(user) for user in users]

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_serializer(user)

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user: User):
    updated_result = await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": user.dict()})
    if updated_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = await users_collection.find_one({"_id": ObjectId(user_id)})
    return user_serializer(updated_user)

@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    deleted_result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    if deleted_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deleted successfully"}
