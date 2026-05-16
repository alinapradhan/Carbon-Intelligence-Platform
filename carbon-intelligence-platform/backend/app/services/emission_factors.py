from dataclasses import dataclass

@dataclass(frozen=True)
class EmissionFactors:
    electricity_kg_per_kwh: dict[str, float]
    fuel_kg_per_liter: float = 2.68
    fleet_kg_per_km: float = 0.19
    logistics_kg_per_km: float = 0.62
    process_kg_per_unit: float = 0.84
    heating_cooling_kg_per_kwh: float = 0.11
    supplier_kg_per_ton_output: float = 44.0
    commuting_kg_per_employee_day: float = 6.8
    waste_kg_per_ton: float = 420.0
    travel_kg_per_ton_output: float = 3.2
    lifecycle_kg_per_ton_output: float = 56.0

DEFAULT_FACTORS = EmissionFactors(
    electricity_kg_per_kwh={
        'Bavaria-DE': 0.31,
        'Midwest-US': 0.42,
        'Shenzhen-CN': 0.55,
        'Nordics-EU': 0.12,
        'TamilNadu-IN': 0.64,
    }
)
