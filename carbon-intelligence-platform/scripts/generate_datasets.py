from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / 'backend'))
from app.simulators.synthetic_data import generate_dataset

if __name__ == '__main__':
    df = generate_dataset(ROOT / 'datasets' / 'industrial_emissions.csv')
    print(f'generated {len(df)} rows at datasets/industrial_emissions.csv')
