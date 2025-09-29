import requests
from datetime import datetime
from typing import Dict, List, Tuple
import logging
from ingestion.config import API_URL, HOURLY_VARIABLES


# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _get_session() -> requests.Session:
    """Create and return a requests session with default headers."""
    session = requests.Session()
    session.headers.update({"User-Agent": "AirQualityClient/1.0"})
    return session


def fetch_air_quality_for_city(city: Dict) -> Tuple[Dict, List[Dict]]:
    """
    Fetch and parse air quality data for a SINGLE city.
    Args:
        city (dict): A dict with keys 'name', 'latitude', and 'longitude'.
    Returns:
        - raw_payload: The raw JSON response from the API.
        - parsed_records: A list of parsed records for that city.
    """
    name = city["name"]
    lat = city["latitude"]
    lon = city["longitude"]

    logger.info(f"🌍 Fetching air quality data for {name}...")

    session = _get_session()
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": HOURLY_VARIABLES
    }

    # --- Request data ---
    response = session.get(API_URL, params=params)
    response.raise_for_status()
    raw_payload = response.json()
    logger.info(f"✅ Raw data fetched for {name}")

    # --- Parse hourly section ---
    hourly = raw_payload.get("hourly", {})
    times = hourly.get("time", [])
    pollutants = [k for k in hourly.keys() if k != "time"]

    parsed_records: List[Dict] = []

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

        parsed_records.append(record)

    logger.info(f"✅ Parsed {len(parsed_records)} records for {name}")
    return raw_payload, parsed_records


if __name__ == "__main__":
    # Example usage for a single city test
    nairobi = {"name": "Nairobi", "latitude": -1.286389, "longitude": 36.817223}
    raw, parsed = fetch_air_quality_for_city(nairobi)
    print(f"✅ Retrieved raw data keys: {list(raw.keys())}")
    print(f"✅ Total parsed records: {len(parsed)}")
    print(parsed[0])
