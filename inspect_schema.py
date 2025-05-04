# inspect_raw.py
import json
from open_air.db import get_conn

with get_conn() as conn:
    cur = conn.cursor()
    # pull 3 AirNow rows
    cur.execute("""
        SELECT payload 
        FROM raw.measurements_raw 
        WHERE provider = 'airnow'
        LIMIT 3
    """)
    airnow_rows = cur.fetchall()

    # pull 3 OpenAQ rows
    cur.execute("""
        SELECT payload 
        FROM raw.measurements_raw 
        WHERE provider = 'openaq'
        LIMIT 3
    """)
    openaq_rows = cur.fetchall()

print("=== AirNow payloads ===")
for (p,) in airnow_rows:
    # payload comes in as a JSON array
    arr = p
    print(json.dumps(arr, indent=2))
    print()

print("=== OpenAQ payloads ===")
for (p,) in openaq_rows:
    print(json.dumps(p, indent=2))
    print()
