# RCA: RAN p95 latency breach
- Impact: burned ~5% monthly error budget (17m breach).
- Root Cause: HPA minReplicas=1 + CPU throttling.
- Fix: minReplicas=3; requests/limits; autoscaling policy.
