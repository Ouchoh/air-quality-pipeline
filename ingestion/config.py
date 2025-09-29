# config.py (place in project root)
from dotenv import load_dotenv
from pathlib import Path
import os

# load .env from project root
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")

if not MONGO_USER or not MONGO_PASS:
    raise RuntimeError("MONGO_USER / MONGO_PASS not set (check .env or environment)")


# ------------------------------------------------------------------------------
# 🌍 Air Quality API Settings
# ------------------------------------------------------------------------------
API_URL = os.getenv("API_URL", "https://air-quality-api.open-meteo.com/v1/air-quality")
HOURLY_VARIABLES = ["pm2_5", "pm10", "ozone", "carbon_monoxide", "nitrogen_dioxide", "sulphur_dioxide"]

# ------------------------------------------------------------------------------
# 🏙️ Cities to Ingest
# ------------------------------------------------------------------------------
CITIES = [
    {"name": "Nairobi", "latitude": -1.286389, "longitude": 36.817223},
    {"name": "Mombasa", "latitude": -4.0435, "longitude": 39.6682},
    {"name": "Kampala", "latitude": 0.3476, "longitude": 32.5825}
]