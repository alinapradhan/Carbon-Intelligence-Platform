from fastapi import APIRouter, Query
from app.analytics.anomaly_detection import detect_anomalies
from app.analytics.kpis import scope_summary, sustainability_kpis, trends
from app.forecasting.model import forecast, train_forecaster
from app.models.database import initialize_database, query_dataframe
from app.models.schemas import Alert, EmissionRecord, ForecastResponse, KPIResponse, ReportResponse, ScopeSummary, TrainResponse
from app.services.recommendations import reduction_recommendations

router = APIRouter()

def emissions_frame():
    initialize_database()
    return query_dataframe('SELECT * FROM emissions ORDER BY date')

@router.get('/emissions/live', response_model=list[EmissionRecord])
def live_emissions(limit: int = Query(25, ge=1, le=250)):
    df = query_dataframe('SELECT * FROM emissions ORDER BY date DESC LIMIT ?', (limit,))
    return df.sort_values('date').to_dict(orient='records')

@router.get('/emissions/scope1', response_model=ScopeSummary)
def scope1():
    return scope_summary(emissions_frame(), 'scope1')

@router.get('/emissions/scope2', response_model=ScopeSummary)
def scope2():
    return scope_summary(emissions_frame(), 'scope2')

@router.get('/emissions/scope3', response_model=ScopeSummary)
def scope3():
    return scope_summary(emissions_frame(), 'scope3')

@router.get('/analytics/kpis', response_model=KPIResponse)
def kpis():
    return sustainability_kpis(emissions_frame())

@router.get('/analytics/trends')
def trend_analysis():
    return trends(emissions_frame())

@router.get('/analytics/forecast', response_model=ForecastResponse)
def forecasting_results(horizon_days: int = Query(30, ge=7, le=120)):
    return forecast(emissions_frame(), horizon_days)

@router.get('/alerts', response_model=list[Alert])
def alerts():
    return detect_anomalies(emissions_frame())

@router.get('/reports', response_model=ReportResponse)
def carbon_report():
    df = emissions_frame()
    kpi = sustainability_kpis(df)
    active_alerts = detect_anomalies(df)
    return {'title': 'Industrial Carbon Intelligence Report', 'period': f"{df['date'].min()} to {df['date'].max()}", 'executive_summary': 'Synthetic multi-facility analysis covering Scope 1, Scope 2, and Scope 3 emissions with renewable contribution, carbon intensity, alerts, and reduction pathways.', 'kpis': kpi, 'recommendations': reduction_recommendations(kpi, active_alerts)}

@router.post('/model/train', response_model=TrainResponse)
def train_model():
    result = train_forecaster(emissions_frame())
    return {'status': 'trained', 'model_path': result['model_path'], 'mae': result['mae'], 'rmse': result['rmse']}
