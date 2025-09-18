# Telco Cloud Project – OpenShift Step-by-Step Guide

This guide explains how to deploy the **RAN/Core simulators** and the **observability stack** on **OpenShift (OKD/OCP)**.

---

## 1. Login to OpenShift
```bash
oc login --token=<your-token> --server=<your-server-URL>
```
📸 *Screenshot placeholder*: OpenShift Web Console login screen.

## 2. Create Projects (Namespaces)
```bash
oc new-project platform
oc new-project ns-ran
oc new-project ns-core
```
📸 *Screenshot placeholder*: Projects list in Web Console.

## 3. Deploy Simulators with Helm (OpenShift values)
```bash
helm upgrade --install ran-sim charts/ran-sim -n ns-ran -f charts/ran-sim/values-openshift.yaml
helm upgrade --install core-sim charts/core-sim -n ns-core -f charts/core-sim/values-openshift.yaml
```
📸 *Screenshot placeholder*: Workloads → Deployments of both apps.

## 4. Expose via Routes
```bash
oc apply -f openshift/routes/ran-sim-route.yaml
oc apply -f openshift/routes/core-sim-route.yaml
```
📸 *Screenshot placeholder*: Route URLs shown in Console.

## 5. Observability
- Import dashboards from `ops/monitoring/dashboards/` into Grafana.
- Verify SLIs: p95 latency, availability, error rate.
📸 *Screenshot placeholder*: Grafana dashboard with metrics.

## 6. OpenShift GitOps (Argo CD)
```bash
oc apply -n openshift-gitops -f openshift/gitops/root-app-openshift.yaml
```
📸 *Screenshot placeholder*: Argo CD app-of-apps tree.

## 7. Tekton (Optional CI)
```bash
oc apply -f ci/tekton/pipeline.yaml
oc apply -f ci/tekton/pipelinerun.yaml
```
📸 *Screenshot placeholder*: PipelineRun status.

## 8. Storage (AWS-backed OpenShift)
```bash
oc apply -f openshift/storage/sc-gp3.yaml
```
📸 *Screenshot placeholder*: StorageClasses page.

## 9. Chaos Drill
```bash
./scripts/chaos/pod-kill.sh ns-ran app=ran-sim
```
📸 *Screenshot placeholder*: Alertmanager firing + pod restart.

