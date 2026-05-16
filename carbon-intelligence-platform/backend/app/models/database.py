from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[3]
DATASET_PATH = BASE_DIR / 'datasets' / 'industrial_emissions.csv'
DB_PATH = Path(__file__).resolve().parents[2] / 'carbon_intelligence.db'

TABLE_SCHEMA = '''
CREATE TABLE IF NOT EXISTS emissions (
  date TEXT, facility_id TEXT, facility_name TEXT, region TEXT, department TEXT,
  electricity_kwh REAL, fuel_liters REAL, renewable_kwh REAL, transport_km REAL,
  process_units REAL, production_output_tons REAL, waste_tons REAL, offsets_tco2e REAL,
  scope1_tco2e REAL, scope2_tco2e REAL, scope3_tco2e REAL, total_tco2e REAL,
  carbon_intensity REAL
);
'''

def connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(TABLE_SCHEMA)
    return conn

def initialize_database(csv_path: Path = DATASET_PATH) -> None:
    from app.simulators.synthetic_data import generate_dataset
    if not csv_path.exists():
        generate_dataset(csv_path=csv_path)
    df = pd.read_csv(csv_path)
    with connection() as conn:
        count = conn.execute('SELECT COUNT(*) FROM emissions').fetchone()[0]
        if count == 0:
            df.to_sql('emissions', conn, if_exists='append', index=False)

def query_dataframe(sql: str, params: tuple = ()) -> pd.DataFrame:
    initialize_database()
    with connection() as conn:
        return pd.read_sql_query(sql, conn, params=params)
