import os
import logging
from typing import List, Dict
from pymongo import MongoClient, ASCENDING, errors
from datetime import datetime
from config import MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_PORT

# -----------------------------------------------------------------------------
# 🔧 Logging
# -----------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# 📦 MongoDB Connection (Secure, No Hardcoded Secrets)
# -----------------------------------------------------------------------------
def get_mongo_client():
    """Create and return a MongoDB client using centralized config variables."""
    if not MONGO_USER or not MONGO_PASS:
        raise ValueError("❌ MongoDB credentials not set. Please check your .env or config.py.")

    mongo_uri = (
        f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin"
    )

    logger.info(f"🔌 Connecting to MongoDB at {MONGO_HOST}:{MONGO_PORT}...")
    client = MongoClient(mongo_uri)
    return client


# -----------------------------------------------------------------------------
# 🗂️ Initialize Collections
# -----------------------------------------------------------------------------
def init_collections():
    """Set up collections and indexes for raw and parsed data."""
    client = get_mongo_client()
    db = client["air_quality_db"]

    raw_collection = db["air_quality_raw"]
    parsed_collection = db["air_quality_parsed"]

    # Create a unique index to avoid duplicates (city + timestamp + pollutant)
    parsed_collection.create_index(
        [("city", ASCENDING), ("timestamp", ASCENDING), ("pollutant", ASCENDING)],
        unique=True
    )

    # Optional: Index for raw payload based on city and fetch time
    raw_collection.create_index(
        [("city", ASCENDING), ("fetched_at", ASCENDING)]
    )

    return raw_collection, parsed_collection

# -----------------------------------------------------------------------------
# 📥 Store Raw Payload
# -----------------------------------------------------------------------------
def save_raw_payload(city: str, raw_data: Dict):
    """Store raw API response for auditing or reprocessing."""
    raw_collection, _ = init_collections()

    doc = {
        "city": city,
        "fetched_at": datetime.utcnow().isoformat(),
        "payload": raw_data
    }

    try:
        raw_collection.insert_one(doc)
        logger.info(f"📦 Raw payload saved for {city}")
    except errors.PyMongoError as e:
        logger.error(f"❌ Failed to save raw payload for {city}: {e}")

# -----------------------------------------------------------------------------
# 📊 Store Parsed Records
# -----------------------------------------------------------------------------
def save_parsed_records(city: str, records: List[Dict]):
    """Store structured air quality records with deduplication."""
    _, parsed_collection = init_collections()
    inserted, skipped = 0, 0

    for record in records:
        for pollutant, value in record.items():
            if pollutant in ["city", "timestamp", "latitude", "longitude", "elevation", "source"]:
                continue

            doc = {
                "city": city,
                "timestamp": record["timestamp"],
                "pollutant": pollutant,
                "value": value,
                "latitude": record["latitude"],
                "longitude": record["longitude"],
                "elevation": record["elevation"],
                "source": record["source"]
            }

            try:
                parsed_collection.insert_one(doc)
                inserted += 1
            except errors.DuplicateKeyError:
                skipped += 1
            except errors.PyMongoError as e:
                logger.error(f"❌ Failed to insert record for {city}: {e}")

    logger.info(f"✅ Parsed data saved for {city}: {inserted} inserted, {skipped} duplicates skipped")

# -----------------------------------------------------------------------------
# ✅ Example Usage (manual testing)
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # Example dummy data (replace with real client.py results)
    raw_example = {"meta": "example payload"}
    parsed_example = [
        {
            "city": "Nairobi",
            "timestamp": "2025-09-26T00:00:00",
            "latitude": -1.2999,
            "longitude": 36.8000,
            "elevation": 1671,
            "source": "open-meteo",
            "pm2_5": 18.2,
            "ozone": 46.0
        }
    ]

    save_raw_payload("Nairobi", raw_example)
    save_parsed_records("Nairobi", parsed_example)
