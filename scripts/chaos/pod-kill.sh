#!/usr/bin/env bash
set -euo pipefail
ns=${1:-ns-ran}; label=${2:-app=ran-sim}
pod=$(kubectl -n "$ns" get pods -l "$label" -o name | head -n1)
echo "Deleting $pod in $ns ..."
kubectl -n "$ns" delete "$pod" --grace-period=0 --force
