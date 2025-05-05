## Warehouse & Metadata

This project ingests raw air‑quality data from AirNow and OpenAQ, transforms it via **dbt**, and stores it in a normalized Postgres schema.  
Key artefacts:

- **dbt docs site** (static): [docs/dbt_site/index.html](docs/dbt_site/index.html)  
- **Entity‑Relationship Diagram**: ![ERD](docs/erd.png)  
- **ISO 19115 XML metadata**: [`docs/metadata/open_air.xml`](docs/metadata/open_air.xml)  
