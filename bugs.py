from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# In-memory data store
users: List[Dict[str, str]] = []

# Pydantic model for request validation
class User(BaseModel):
    name: str
    email: str

@app.post("/users/")
def create_user(user: User):
    # Bug: Incorrect ID generation (should be len(users) + 1)
    new_user = {
        "id": len(users),  # Bug: This will cause duplicate IDs
        "name": user.name,
        "email": user.email
    }
    users.append(new_user)
    return {"message": "User created successfully", "user": new_user}

@app.get("/users/")
def get_users():
    # Bug: Incorrect key used in response (should be "users")
    return {"user_list": users}  # Bug: Wrong key used

@app.get("/users/{user_id}")
def get_user(user_id: int):
    # Bug: Missing proper user check (fails on empty list)
    user = next((u for u in users if u["id"] == user_id))  # Bug: Throws StopIteration if not found
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    for user in users:
        if user["id"] == user_id:
            user["name"] = updated_user.name
            user["email"] = updated_user.email
            return {"message": "User updated successfully", "user": user}
    # Bug: Wrong status code (should be 404)
    raise HTTPException(status_code=400, detail="User not found")  # Bug: Incorrect HTTP status code

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    global users
    # Bug: Incorrect deletion logic (doesn't filter correctly)
    users = [user for user in users if user["id"] == user_id]  # Bug: Should be != instead of ==
    return {"message": "User deleted successfully"}
