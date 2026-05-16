from pathlib import Path
import numpy as np
import pandas as pd
from app.services.carbon_engine import CarbonCalculationEngine

FACILITIES = [
    ('FAC-DE-01', 'Digital Motor Works', 'Bavaria-DE', 'Assembly'),
    ('FAC-US-02', 'Grid Automation Plant', 'Midwest-US', 'Electronics'),
    ('FAC-CN-03', 'Industrial Drives Campus', 'Shenzhen-CN', 'Machining'),
    ('FAC-EU-04', 'Nordic Smart Factory', 'Nordics-EU', 'Robotics'),
    ('FAC-IN-05', 'Process Controls Hub', 'TamilNadu-IN', 'Testing'),
]

def generate_dataset(csv_path: Path, days: int = 540, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=days, freq='D')
    rows = []
    for facility_id, name, region, department in FACILITIES:
        scale = rng.uniform(0.75, 1.35)
        inefficiency = rng.uniform(0.92, 1.16)
        for i, day in enumerate(dates):
            weekday = 1.0 if day.weekday() < 5 else 0.62
            seasonal = 1 + 0.18 * np.sin(2 * np.pi * day.dayofyear / 365)
            production_cycle = 1 + 0.12 * np.sin(2 * np.pi * i / 14)
            peak = 1.25 if 9 <= (i % 24) <= 17 else 1.0
            maintenance_drag = 1.18 if i % 97 in (0, 1, 2) else 1.0
            production = max(35, rng.normal(170 * scale * weekday * production_cycle, 18))
            electricity = rng.normal(3100 * scale * seasonal * weekday * peak * maintenance_drag, 240)
            renewable = electricity * np.clip(rng.normal(0.28 + 0.17 * np.sin(2*np.pi*(day.dayofyear+30)/365), 0.08), 0.04, 0.62)
            fuel = rng.normal(430 * scale * weekday * inefficiency, 45)
            transport = rng.normal(760 * scale * weekday, 90)
            process_units = production * rng.normal(7.6 * inefficiency, 0.45)
            waste = max(0.8, rng.normal(production * 0.055 * inefficiency, 1.4))
            offsets = max(0, rng.normal(2.8 * scale + renewable / 2400, 0.8))
            if i % 121 == 0:
                electricity *= 1.55
                fuel *= 1.35
            rows.append({
                'date': day.date().isoformat(), 'facility_id': facility_id, 'facility_name': name,
                'region': region, 'department': department, 'electricity_kwh': round(float(electricity), 2),
                'fuel_liters': round(float(fuel), 2), 'renewable_kwh': round(float(renewable), 2),
                'transport_km': round(float(transport), 2), 'process_units': round(float(process_units), 2),
                'production_output_tons': round(float(production), 2), 'waste_tons': round(float(waste), 2),
                'offsets_tco2e': round(float(offsets), 3), 'employee_count': int(rng.integers(95, 240))
            })
    df = pd.DataFrame(rows)
    df = CarbonCalculationEngine().calculate(df)
    out = df.drop(columns=['employee_count'])
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(csv_path, index=False)
    return out

if __name__ == '__main__':
    generate_dataset(Path(__file__).resolve().parents[3] / 'datasets' / 'industrial_emissions.csv')
