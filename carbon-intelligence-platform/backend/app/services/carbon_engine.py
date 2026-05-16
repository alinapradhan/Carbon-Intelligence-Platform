import pandas as pd
from app.services.emission_factors import DEFAULT_FACTORS, EmissionFactors

class CarbonCalculationEngine:
    def __init__(self, factors: EmissionFactors = DEFAULT_FACTORS):
        self.factors = factors

    def calculate(self, frame: pd.DataFrame) -> pd.DataFrame:
        df = frame.copy()
        grid_factor = df['region'].map(self.factors.electricity_kg_per_kwh).fillna(0.4)
        net_grid_kwh = (df['electricity_kwh'] - df['renewable_kwh']).clip(lower=0)
        scope1_kg = (
            df['fuel_liters'] * self.factors.fuel_kg_per_liter
            + df['transport_km'] * self.factors.fleet_kg_per_km
            + df['process_units'] * self.factors.process_kg_per_unit
        )
        scope2_kg = net_grid_kwh * grid_factor + df['electricity_kwh'] * 0.18 * self.factors.heating_cooling_kg_per_kwh
        scope3_kg = (
            df['production_output_tons'] * self.factors.supplier_kg_per_ton_output
            + df['transport_km'] * self.factors.logistics_kg_per_km
            + df.get('employee_count', 120) * self.factors.commuting_kg_per_employee_day
            + df['waste_tons'] * self.factors.waste_kg_per_ton
            + df['production_output_tons'] * self.factors.travel_kg_per_ton_output
            + df['production_output_tons'] * self.factors.lifecycle_kg_per_ton_output
        )
        df['scope1_tco2e'] = scope1_kg / 1000
        df['scope2_tco2e'] = scope2_kg / 1000
        df['scope3_tco2e'] = scope3_kg / 1000
        df['total_tco2e'] = df[['scope1_tco2e', 'scope2_tco2e', 'scope3_tco2e']].sum(axis=1) - df['offsets_tco2e']
        df['carbon_intensity'] = df['total_tco2e'] / df['production_output_tons'].clip(lower=1)
        return df
