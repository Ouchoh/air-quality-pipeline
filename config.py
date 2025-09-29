# config.py (place in project root)
from dotenv import load_dotenv
from pathlib import Path
import os

# load .env from project root
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")

if not MONGO_USER or not MONGO_PASS:
    raise RuntimeError("MONGO_USER / MONGO_PASS not set (check .env or environment)")
