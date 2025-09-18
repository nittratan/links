from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import urllib.parse
import logging
import os

logger = logging.getLogger(__name__)

# Optionally use environment variables for credentials
DB_USER = os.getenv("PIINV_DB_USER", "PIINV_08_USER")
DB_PASS = os.getenv("PIINV_DB_PASS", "PIINV_DB_PASS")
DB_HOST = os.getenv("PIINV_DB_HOST", "PIINV_DB_HOST")
DB_PORT = os.getenv("PIINV_DB_PORT", "PIINV_DB_PORT")
DB_NAME = os.getenv("PIINV_DB_NAME", "PIINV_DB_NAME")


class Database:
    _engine = None
    _SessionLocal = None

    @classmethod
    def init(cls):
        """
        Initialize DB connection once at startup.
        """
        try:
            encoded_password = urllib.parse.quote_plus(str(DB_PASS))
            DATABASE_URL = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

            cls._engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20)
            cls._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls._engine)

            # Test connection
            with cls._engine.connect() as conn:
                conn.execute("SELECT 1")
            logger.info("Database connection initialized successfully ✅")
        except Exception as e:
            logger.error(f"Error initializing DB connection: {e}")
            cls._engine = None
            cls._SessionLocal = None

    @classmethod
    def get_session(cls) -> Session:
        if cls._SessionLocal is None:
            logger.error("DB connection not initialized!")
            return None
        return cls._SessionLocal()


from fastapi import FastAPI
from connection import Database

app = FastAPI()

@app.on_event("startup")
def startup_event():
    # Initialize DB connection once
    Database.init()

@app.get("/items/")
def read_items():
    db = Database.get_session()
    if not db:
        return {"error": "DB connection not available"}
    
    result = db.execute("SELECT * FROM items LIMIT 10").fetchall()
    db.close()
    return {"items": result}


