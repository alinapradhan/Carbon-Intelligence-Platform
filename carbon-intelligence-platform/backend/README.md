# Backend

FastAPI backend for local industrial carbon intelligence. Run from this directory with:

```bash
uvicorn app.main:app --reload
```

The API initializes `carbon_intelligence.db` from `../datasets/industrial_emissions.csv` on startup.
