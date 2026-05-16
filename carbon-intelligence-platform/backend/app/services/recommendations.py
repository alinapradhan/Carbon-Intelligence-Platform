def reduction_recommendations(kpis: dict, alerts: list[dict]) -> list[str]:
    recs = []
    if kpis['renewable_share_pct'] < 35:
        recs.append('Increase renewable power purchase agreements and schedule flexible loads during high renewable availability windows.')
    if kpis['carbon_intensity_tco2e_per_ton'] > 0.08:
        recs.append('Prioritize compressed-air leak audits, high-efficiency drives, and predictive maintenance on energy-intensive lines.')
    if any(a['category'] == 'emissions_spike' for a in alerts):
        recs.append('Investigate facilities with emissions spikes and compare equipment telemetry against maintenance calendars.')
    recs.append('Use facility-level marginal abatement curves to rank electrification, waste diversion, logistics optimization, and offset projects.')
    return recs
