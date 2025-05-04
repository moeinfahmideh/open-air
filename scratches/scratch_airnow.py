import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv()


API = "https://www.airnowapi.org/aq/observation/latLong/current/"
params = {
    "format": "application/json",
    "latitude": 40.7128,  # New York City
    "longitude": -74.0060,
    "distance": 25,  # miles
    "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    "API_KEY": os.getenv("AIRNOW_API_KEY"),
}
print(requests.get(API, params=params, timeout=10).json()[0])
