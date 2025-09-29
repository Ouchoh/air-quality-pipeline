import requests
from datetime import datetime
from typing import Dict, List, Tuple
import logging

# --- Config ---
API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
HOURLY_VARIABLES = ["pm2_5", "pm10", "ozone", "carbon_monoxide", "nitrogen_dioxide", "sulphur_dioxide"]

# Define all target cities here
CITIES = [
    {"name": "Nairobi", "latitude": -1.286389, "longitude": 36.817223},
    {"name": "Mombasa", "latitude": -4.0435, "longitude": 39.6682}
]

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# --- Helper to reuse connections ---
def _get_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": "AirQualityClient/1.0"})
    return session


def fetch_air_quality_for_all() -> Tuple[Dict[str, Dict], List[Dict]]:
    """
    Fetches air quality data for multiple cities (Nairobi, Mombasa) in one run.
    Returns:
      - raw_payloads: dict with raw JSON per city
      - all_parsed_records: list of parsed records for all cities combined
    """
    session = _get_session()
    raw_payloads: Dict[str, Dict] = {}
    all_parsed_records: List[Dict] = []

    for city in CITIES:
        name = city["name"]
        lat = city["latitude"]
        lon = city["longitude"]

        logger.info(f"🌍 Fetching air quality data for {name}...")
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": HOURLY_VARIABLES
        }

        # --- Request data ---
        response = session.get(API_URL, params=params)
        response.raise_for_status()
        raw_payload = response.json()
        raw_payloads[name] = raw_payload
        logger.info(f"✅ Raw data fetched for {name}")

        # --- Parse hourly section ---
        hourly = raw_payload.get("hourly", {})
        times = hourly.get("time", [])
        pollutants = [k for k in hourly.keys() if k != "time"]

        for i, timestamp in enumerate(times):
            record = {
                "city": name,
                "timestamp": datetime.fromisoformat(timestamp).isoformat(),
                "latitude": raw_payload.get("latitude"),
                "longitude": raw_payload.get("longitude"),
                "elevation": raw_payload.get("elevation"),
                "source": "open-meteo"
            }
            # Add pollutant readings
            for p in pollutants:
                values = hourly.get(p, [])
                record[p] = values[i] if i < len(values) else None

            all_parsed_records.append(record)

        logger.info(f"✅ Parsed {len(times)} records for {name}")

    logger.info(f"🎉 Finished fetching data for {len(CITIES)} cities.")
    return raw_payloads, all_parsed_records


if __name__ == "__main__":
    raw, parsed = fetch_air_quality_for_all()
    print(f"✅ Retrieved raw data for: {list(raw.keys())}")
    print(f"✅ Total parsed records: {len(parsed)}")
    # Optional: print first record for inspection
    print(parsed[0])
