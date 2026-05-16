from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

MODEL_PATH = Path(__file__).resolve().parents[3] / 'ml' / 'emissions_forecaster.joblib'

def _features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    data = df.copy()
    data['date'] = pd.to_datetime(data['date'])
    data = data.groupby('date', as_index=False).agg({'total_tco2e':'sum','electricity_kwh':'sum','renewable_kwh':'sum','production_output_tons':'sum','fuel_liters':'sum','transport_km':'sum'})
    data['dayofweek'] = data['date'].dt.dayofweek
    data['month'] = data['date'].dt.month
    data['lag_1'] = data['total_tco2e'].shift(1).bfill()
    data['lag_7'] = data['total_tco2e'].shift(7).bfill()
    data['rolling_7'] = data['total_tco2e'].rolling(7, min_periods=1).mean()
    x = data[['electricity_kwh','renewable_kwh','production_output_tons','fuel_liters','transport_km','dayofweek','month','lag_1','lag_7','rolling_7']]
    return x, data['total_tco2e']

def train_forecaster(df: pd.DataFrame) -> dict:
    x, y = _features(df)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.22, shuffle=False)
    model = RandomForestRegressor(n_estimators=180, random_state=7, min_samples_leaf=3)
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return {'model': model, 'mae': float(mean_absolute_error(y_test, pred)), 'rmse': float(np.sqrt(mean_squared_error(y_test, pred))), 'model_path': str(MODEL_PATH)}

def forecast(df: pd.DataFrame, horizon_days: int = 30) -> dict:
    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)
        metrics = {'mae': 0.0, 'rmse': 0.0}
    else:
        trained = train_forecaster(df)
        model, metrics = trained['model'], {'mae': trained['mae'], 'rmse': trained['rmse']}
    daily = df.copy(); daily['date'] = pd.to_datetime(daily['date'])
    daily = daily.groupby('date', as_index=False).agg({'total_tco2e':'sum','electricity_kwh':'sum','renewable_kwh':'sum','production_output_tons':'sum','fuel_liters':'sum','transport_km':'sum'})
    last = daily.tail(14).copy()
    points = []
    for step in range(1, horizon_days + 1):
        next_date = daily['date'].max() + pd.Timedelta(days=step)
        recent = last.tail(7)
        row = pd.DataFrame([{ 'electricity_kwh': recent['electricity_kwh'].mean()*1.002, 'renewable_kwh': recent['renewable_kwh'].mean()*1.004, 'production_output_tons': recent['production_output_tons'].mean()*1.001, 'fuel_liters': recent['fuel_liters'].mean()*.999, 'transport_km': recent['transport_km'].mean()*1.001, 'dayofweek': next_date.dayofweek, 'month': next_date.month, 'lag_1': last['total_tco2e'].iloc[-1], 'lag_7': last['total_tco2e'].iloc[-7], 'rolling_7': recent['total_tco2e'].mean()}])
        pred = float(model.predict(row)[0])
        points.append({'date': next_date.date().isoformat(), 'predicted_emissions_tco2e': round(pred, 2), 'predicted_energy_kwh': round(float(row['electricity_kwh'].iloc[0]), 2)})
        last = pd.concat([last, pd.DataFrame([{**row.iloc[0].to_dict(), 'date': next_date, 'total_tco2e': pred}])], ignore_index=True)
    return {'mae': round(metrics['mae'], 3), 'rmse': round(metrics['rmse'], 3), 'horizon_days': horizon_days, 'forecast': points}
