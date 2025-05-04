from open_air.db import get_conn
with get_conn() as conn:
    cur = conn.cursor()
    cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_schema='clean' AND table_name='stg_airnow_measurements';")
    print(cur.fetchall())
    cur.execute("SELECT * FROM clean.stg_airnow_measurements LIMIT 5;")
    print(cur.fetchall())
