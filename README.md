# Air Quality Data Pipeline

This project is a real-time, containerized data pipeline that ingests, stores, streams, and analyzes air quality metrics for **Nairobi** and **Mombasa**. It uses the [Open-Meteo Air Quality API](https://open-meteo.com/) and processes data for metrics such as PM2.5, PM10, O₃, CO, NO₂, SO₂, and UV index.

**Pipeline Flow:**  
API → MongoDB → Kafka → Cassandra → Dashboard

	Tech Stack
- Python (Ingestion, Stream Processing)
- MongoDB (Raw & curated data storage)
- Kafka (Streaming & event transport)
- Cassandra (Low-latency analytics)
- Docker & Docker Compose (Container orchestration)
- Grafana / Metabase (Dashboard visualization)


	Project Structure
.
├── ingestion/        # API ingestion service
├── streaming/        # Kafka producers/consumers
├── storage/          # Cassandra writers
├── docker/           # Dockerfiles & docker-compose
├── dashboards/       # Dashboard configs or queries
├── docs/             # Architecture & data model docs
├── tests/            # Unit & integration tests
├── requirements.txt
├── Makefile
└── README.md

	Getting Started
## 1. Clone the repo
git clone https://github.com/<your-username>/air-quality-pipeline.git
cd air-quality-pipeline

## 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

## 3. Install dependencies
pip install -r requirements.txt

## 4. Configure environment variables
cp .env.example .env
# Update values inside .env with your credentials

## 5. Run with Docker Compose
docker-compose up --build

	Pipeline Architecture
**Data Flow:**
1. Ingestion service pulls hourly air quality data from the Open-Meteo API.
2. Data is stored in MongoDB (raw + curated collections).
3. MongoDB Change Streams or a producer push data into Kafka topics.
4. Kafka consumers write data into Cassandra for fast queries.
5. Dashboards (Grafana/Metabase) query Cassandra for real-time insights.

	
