import asyncio
import json
import os
from datetime import datetime, timezone

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from open_air.db import get_conn

API = "https://www.airnowapi.org/aq/observation/latLong/current/"


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2))
async def _fetch_one(lat: float, lon: float) -> list[dict]:
    params = {
        "format": "application/json",
        "latitude": lat,
        "longitude": lon,
        "distance": 25,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "API_KEY": os.getenv("AIRNOW_API_KEY"),
    }
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(API, params=params)
        r.raise_for_status()
        return r.json()


async def ingest_async():
    records = await _fetch_one(40.7128, -74.0060)  # NYC
    if not records:
        return 0
    with get_conn() as cn:
        # 1 JSON array → rows
        cn.execute(
            """
            INSERT INTO raw.measurements_raw (provider, payload)
            SELECT 'airnow', jsonb_strip_nulls(data)
            FROM jsonb_array_elements(%s::jsonb) AS t(data)
            """,
            (json.dumps(records),),
        )
    return len(records)


def ingest_sync():
    """Sync wrapper for Airflow."""
    return asyncio.run(ingest_async())
