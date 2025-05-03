import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import asyncio
from open_air.ingest import airnow, openaq


def test_airnow_smoke(monkeypatch):
    async def fake_fetch(*_):
        return [{"foo": "bar"}]
    monkeypatch.setattr(airnow, "_fetch_one", fake_fetch)
    inserted = asyncio.run(airnow.ingest())
    assert inserted == 1

def test_openaq_smoke(monkeypatch):
    async def fake_locs(*_): return [1]
    async def fake_meas(*_): return {"results": [{"x": 1}]}
    monkeypatch.setattr(openaq, "_get_locations", fake_locs)
    monkeypatch.setattr(openaq, "_get_measurements", fake_meas)
    inserted = asyncio.run(openaq.ingest())
    assert inserted == 1
