import pandas as pd

def detect_anomalies(df: pd.DataFrame) -> list[dict]:
    alerts: list[dict] = []
    for facility, group in df.sort_values('date').groupby('facility_id'):
        rolling = group['total_tco2e'].rolling(21, min_periods=7)
        baseline = rolling.mean()
        std = rolling.std().fillna(0)
        for idx, row in group.tail(90).iterrows():
            base = float(baseline.loc[idx]) if idx in baseline.index else float(group['total_tco2e'].mean())
            deviation = float(row['total_tco2e']) - base
            if std.loc[idx] and deviation > 2.5 * float(std.loc[idx]):
                alerts.append(_alert(row, 'critical', 'emissions_spike', 'Sudden emissions spike above rolling operating envelope.', base))
            if row['carbon_intensity'] > group['carbon_intensity'].quantile(.94):
                alerts.append(_alert(row, 'warning', 'carbon_intensity', 'High carbon intensity indicates inefficient operations.', float(group['carbon_intensity'].median()), 'carbon_intensity'))
            renewable_share = row['renewable_kwh'] / max(row['electricity_kwh'], 1)
            if renewable_share < .12:
                alerts.append(_alert(row, 'warning', 'renewable_regression', 'Renewable contribution dropped below expected threshold.', .25, 'renewable_kwh'))
    return sorted(alerts, key=lambda x: x['date'], reverse=True)[:40]

def _alert(row, severity: str, category: str, message: str, baseline: float, value_col: str = 'total_tco2e') -> dict:
    return {'date': str(row['date']), 'facility_id': row['facility_id'], 'severity': severity, 'category': category, 'message': message, 'observed_value': round(float(row[value_col]), 3), 'baseline_value': round(float(baseline), 3)}
