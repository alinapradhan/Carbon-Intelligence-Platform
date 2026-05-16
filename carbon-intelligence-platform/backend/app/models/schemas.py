from datetime import date
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class EmissionRecord(BaseModel):
    date: date
    facility_id: str
    facility_name: str
    region: str
    department: str
    electricity_kwh: float
    fuel_liters: float
    renewable_kwh: float
    transport_km: float
    process_units: float
    production_output_tons: float
    waste_tons: float
    offsets_tco2e: float
    scope1_tco2e: float
    scope2_tco2e: float
    scope3_tco2e: float
    total_tco2e: float
    carbon_intensity: float

class ScopeSummary(BaseModel):
    scope: str
    total_tco2e: float
    by_facility: Dict[str, float]
    by_department: Dict[str, float]
    leading_sources: Dict[str, float]

class KPIResponse(BaseModel):
    total_emissions_tco2e: float
    net_emissions_tco2e: float
    renewable_share_pct: float
    carbon_intensity_tco2e_per_ton: float
    net_zero_progress_pct: float
    offsets_tco2e: float

class ForecastPoint(BaseModel):
    date: str
    predicted_emissions_tco2e: float
    predicted_energy_kwh: float

class ForecastResponse(BaseModel):
    mae: float
    rmse: float
    horizon_days: int
    forecast: List[ForecastPoint]

class Alert(BaseModel):
    date: str
    facility_id: str
    severity: str
    category: str
    message: str
    observed_value: float
    baseline_value: float

class ReportResponse(BaseModel):
    title: str
    period: str
    executive_summary: str
    kpis: KPIResponse
    recommendations: List[str]

class TrainResponse(BaseModel):
    status: str
    model_path: str
    mae: float
    rmse: float
