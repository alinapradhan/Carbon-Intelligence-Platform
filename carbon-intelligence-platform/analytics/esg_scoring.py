def esg_score(renewable_share_pct: float, carbon_intensity: float, net_zero_progress_pct: float, alert_count: int) -> dict:
    renewable_component = min(30, renewable_share_pct * 0.75)
    intensity_component = max(0, 35 - carbon_intensity * 180)
    progress_component = min(25, net_zero_progress_pct * 0.25)
    risk_component = max(0, 10 - alert_count * 0.7)
    score = round(renewable_component + intensity_component + progress_component + risk_component, 1)
    rating = 'A' if score >= 85 else 'B' if score >= 70 else 'C' if score >= 55 else 'D'
    return {'score': score, 'rating': rating}
