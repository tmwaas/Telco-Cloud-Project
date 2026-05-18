# Runbook: RAN/Core App Restart
1. Check alert details (Alertmanager).
2. Inspect pods:
   kubectl -n ns-ran get pods -l app=ran-sim
   kubectl -n ns-core get pods -l app=core-sim
3. Restart if needed (rollout restart).
4. Verify /healthz & /metrics.
5. RCA if error budget impacted.
