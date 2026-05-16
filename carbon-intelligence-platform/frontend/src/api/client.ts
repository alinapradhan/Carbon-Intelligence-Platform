import type { Alert, EmissionRecord, ForecastResponse, KPIResponse, ScopeSummary } from '../types';
const API = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';
async function get<T>(path: string): Promise<T> { const res = await fetch(`${API}${path}`); if (!res.ok) throw new Error(`API ${path} failed`); return res.json(); }
export const carbonApi = { live: () => get<EmissionRecord[]>('/emissions/live?limit=80'), kpis: () => get<KPIResponse>('/analytics/kpis'), trends: () => get<any[]>('/analytics/trends'), forecast: () => get<ForecastResponse>('/analytics/forecast?horizon_days=30'), alerts: () => get<Alert[]>('/alerts'), scope: (n: 1|2|3) => get<ScopeSummary>(`/emissions/scope${n}`) };
