import requests
from pydantic import BaseModel
from typing import List
import json

class TodoItem(BaseModel):
    userId: int
    id: int
    title: str
    completed: bool

def fetch_todos() -> List[TodoItem]:
    response = requests.get("https://jsonplaceholder.typicode.com/todos/")
    response.raise_for_status()  # Raise an error for non-200 status codes
    todos_data = response.json()
    todos = [TodoItem(**todo) for todo in todos_data]
    return todos

def dump_to_json(data: List[TodoItem], filename: str):
    with open(filename, 'w') as file:
        json.dump([todo.dict() for todo in data], file, indent=4)

if __name__ == "__main__":
    todos = fetch_todos()
    dump_to_json(todos, "todos.json")
