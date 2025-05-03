import json, os, httpx, asyncio
from tenacity import retry, stop_after_attempt, wait_exponential
from open_air.db import get_conn

URL_BASE = "https://api.openaq.org/v3"
HEADERS = {"X-API-Key": os.getenv("OPENAQ_API_KEY")}

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2))
async def _get_locations(lat: float, lon: float, radius_m=25000) -> list[int]:
    url = f"{URL_BASE}/locations"
    params = dict(coordinates=f"{lat},{lon}", radius=radius_m, limit=100)
    async with httpx.AsyncClient(timeout=15, headers=HEADERS) as c:
        res = await c.get(url, params=params)
        res.raise_for_status()
        return [loc["id"] for loc in res.json()["results"]]

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2))
async def _get_measurements(loc_id: int) -> dict:
    url = f"{URL_BASE}/locations/{loc_id}/measurements"
    async with httpx.AsyncClient(timeout=15, headers=HEADERS) as c:
        res = await c.get(url, params={"limit": 1})
        res.raise_for_status()
        return res.json()

async def ingest(lat=51.5072, lon=-0.1276):
    loc_ids = await _get_locations(lat, lon)
    if not loc_ids:
        return 0
    async def gather_measurements():
        tasks = [_get_measurements(lid) for lid in loc_ids]
        return await asyncio.gather(*tasks, return_exceptions=False)
    bundles = await gather_measurements()
    # Flatten any empty results
    records = [row for b in bundles for row in b.get("results", [])]
    if not records:
        return 0
    with get_conn() as cn:
        cn.execute(
            """
            INSERT INTO raw.measurements_raw (provider, payload)
            VALUES ('openaq', %s)
            """,
            (json.dumps(records),),
        )
    return len(records)

if __name__ == "__main__":
    print(asyncio.run(ingest()), "openaq rows inserted")
