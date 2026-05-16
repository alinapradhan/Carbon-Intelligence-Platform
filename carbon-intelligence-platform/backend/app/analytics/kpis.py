import pandas as pd

def scope_summary(df: pd.DataFrame, scope: str) -> dict:
    col = f'{scope}_tco2e'
    return {
        'scope': scope.upper(),
        'total_tco2e': round(float(df[col].sum()), 2),
        'by_facility': df.groupby('facility_name')[col].sum().round(2).to_dict(),
        'by_department': df.groupby('department')[col].sum().round(2).to_dict(),
        'leading_sources': _sources(df, scope),
    }

def sustainability_kpis(df: pd.DataFrame) -> dict:
    total = float(df['total_tco2e'].sum())
    offsets = float(df['offsets_tco2e'].sum())
    renewable_share = 100 * float(df['renewable_kwh'].sum()) / max(float(df['electricity_kwh'].sum()), 1)
    intensity = total / max(float(df['production_output_tons'].sum()), 1)
    baseline = float(df.head(max(len(df)//5, 1))['total_tco2e'].mean())
    recent = float(df.tail(max(len(df)//5, 1))['total_tco2e'].mean())
    progress = max(0, min(100, (baseline - recent) / max(baseline * 0.45, 1) * 100))
    return {
        'total_emissions_tco2e': round(total, 2),
        'net_emissions_tco2e': round(total - offsets, 2),
        'renewable_share_pct': round(renewable_share, 2),
        'carbon_intensity_tco2e_per_ton': round(intensity, 4),
        'net_zero_progress_pct': round(progress, 2),
        'offsets_tco2e': round(offsets, 2),
    }

def trends(df: pd.DataFrame) -> list[dict]:
    daily = df.groupby('date', as_index=False).agg({
        'total_tco2e': 'sum', 'scope1_tco2e': 'sum', 'scope2_tco2e': 'sum', 'scope3_tco2e': 'sum',
        'electricity_kwh': 'sum', 'renewable_kwh': 'sum', 'production_output_tons': 'sum'
    })
    daily['renewable_share_pct'] = 100 * daily['renewable_kwh'] / daily['electricity_kwh'].clip(lower=1)
    return daily.tail(120).round(3).to_dict(orient='records')

def _sources(df: pd.DataFrame, scope: str) -> dict:
    if scope == 'scope1':
        return {'fuel_combustion': round(float(df['fuel_liters'].sum() * 2.68 / 1000), 2), 'owned_vehicle_fleet': round(float(df['transport_km'].sum() * .19 / 1000), 2), 'industrial_processes': round(float(df['process_units'].sum() * .84 / 1000), 2)}
    if scope == 'scope2':
        return {'purchased_electricity': round(float(df['scope2_tco2e'].sum() * .82), 2), 'heating_and_cooling': round(float(df['scope2_tco2e'].sum() * .18), 2)}
    return {'supplier_activity': round(float(df['production_output_tons'].sum() * 44 / 1000), 2), 'logistics': round(float(df['transport_km'].sum() * .62 / 1000), 2), 'waste_and_lifecycle': round(float(df['scope3_tco2e'].sum() * .55), 2)}
