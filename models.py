from sqlalchemy import (
    MetaData, Table, Column,
    Integer, Numeric, Text, TIMESTAMP, ForeignKey
)
from sqlalchemy.dialects.postgresql import TIMESTAMP as PG_TZ, NUMERIC
from sqlalchemy import create_engine

# load your .env or hardcode the URL
from open_air.db import get_conn
import os

DB_URL = os.getenv("DATABASE_URL", 
       "postgresql://air:@localhost:5432/openair")

engine = create_engine(DB_URL)
meta = MetaData()

locations = Table(
    "locations", meta,
    Column("location_id", Integer, primary_key=True),
    Column("name", Text),
    Column("lat", Numeric(9,6)),
    Column("lon", Numeric(9,6)),
    Column("country_code", Text),
    schema="clean"
)

sensors = Table(
    "sensors", meta,
    Column("sensor_id", Integer, primary_key=True),
    Column("location_id", Integer, ForeignKey("clean.locations.location_id")),
    Column("provider", Text, nullable=False),
    Column("parameter", Text, nullable=False),
    Column("unit", Text),
    schema="clean"
)

measurements = Table(
    "measurements", meta,
    Column("sensor_id", Integer, nullable=False),
    Column("observed_at", PG_TZ, nullable=False),
    Column("value", NUMERIC(10,2)),
    Column("aqi", Integer),
    schema="clean",
    postgresql_partition_by="RANGE (observed_at)"
)

# Note: SQLAlchemy doesn’t manage creating child partitions
# So you’d still issue raw DDL for the partitions AFTER this.

if __name__ == "__main__":
    # Create schema and parent tables
    engine.execute("CREATE SCHEMA IF NOT EXISTS clean;")
    meta.create_all(engine)
    # Then issue the partition DDL:
    engine.execute("""
      CREATE TABLE IF NOT EXISTS clean.measurements_2025_05
      PARTITION OF clean.measurements
      FOR VALUES FROM ('2025-05-01') TO ('2025-06-01');
    """)
    print("✅ clean schema created via SQLAlchemy")
