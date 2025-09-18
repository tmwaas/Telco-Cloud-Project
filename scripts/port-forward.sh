#!/usr/bin/env bash
set -euo pipefail
app=${1:-grafana}; port=${2:-3000}; ns=${3:-platform}
kubectl -n "$ns" port-forward svc/$app $port:80
