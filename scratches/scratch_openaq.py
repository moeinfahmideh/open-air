# scratch_openaq.py
import os
import pprint

import requests
from dotenv import load_dotenv

load_dotenv()
headers = {"X-API-Key": os.getenv("OPENAQ_API_KEY")}
url = "https://api.openaq.org/v3/locations"
params = {
    "coordinates": "51.5072,-0.1276",  # London lat,lon
    "radius": 25000,  # 25 km – max allowed
    "parameters": "pm25",
    "limit": 100,
}

data = requests.get(url, params=params, headers=headers, timeout=10).json()
pprint.pp(data["results"][0])
