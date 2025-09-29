"""
pipeline.py - Orchestrates full air quality data pipeline:
1. Fetch data for multiple cities
2. Store raw payloads into MongoDB
3. Store parsed records into MongoDB
"""

import logging
from datetime import datetime
from typing import Dict, List

# --- Import from our modules ---
from ingestion.client import fetch_air_quality_for_city
from ingestion.storage import save_raw_payload, save_parsed_records
from ingestion.config import CITIES

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pipeline")


def run_pipeline() -> None:
    """
    Main entrypoint: fetch, parse, and store air quality data for all cities.
    """
    logger.info("🚀 Starting air quality ingestion pipeline...")

    total_raw = 0
    total_parsed = 0

    for city in CITIES:
        city_name = city["name"]
        logger.info(f"🌍 Processing city: {city_name}")

        try:
            # --- 1️⃣ Fetch & parse ---
            raw_payload, parsed_records = fetch_air_quality_for_city(city)

            # --- 2️⃣ Save raw payload ---
            save_raw_payload(city_name, raw_payload)
            total_raw += 1

            # --- 3️⃣ Save parsed records ---
            save_parsed_records(city_name, parsed_records)
            total_parsed += len(parsed_records)

            logger.info(
                f"✅ Done with {city_name}: {len(parsed_records)} records stored."
            )

        except Exception as e:
            logger.error(f"❌ Failed for {city_name}: {e}", exc_info=True)

    logger.info(
        f"🎉 Pipeline completed: {total_raw} raw payloads and {total_parsed} parsed records stored at {datetime.utcnow().isoformat()}"
    )


if __name__ == "__main__":
    run_pipeline()
