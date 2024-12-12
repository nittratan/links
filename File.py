import logging
from fastapi import FastAPI
from routes.pdf_routes import router

# Initialize FastAPI app
app = FastAPI()

# Include router from routes
app.include_router(router)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
