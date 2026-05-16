# Architecture Notes

The platform is intentionally local-only. It excludes cloud hosting, Kubernetes, Docker orchestration, authentication, enterprise SSO, CI/CD, and production infrastructure so the repository stays focused on sustainability analytics and clean implementation.

## Bounded Contexts

- **Simulation** creates realistic industrial telemetry patterns for facilities, regions, production departments, renewable intermittency, and inefficient equipment windows.
- **Carbon accounting** maps operational activity to Scope 1, Scope 2, and Scope 3 emissions using configurable emission factors.
- **Analytics** aggregates total footprint, carbon intensity, renewable share, facility comparisons, net-zero progress, and ESG signals.
- **Forecasting** trains a local scikit-learn time-series model with lag and rolling-window features.
- **Anomaly detection** identifies emissions spikes, abnormal consumption, carbon intensity regressions, and renewable shortfalls.
- **Frontend dashboard** presents an executive industrial cockpit using React, TypeScript, TailwindCSS, and Recharts.
