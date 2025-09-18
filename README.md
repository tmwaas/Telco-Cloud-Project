# Telco Cloud Project – RAN/Core on Kubernetes

This repository focuses on running telecom workloads (RAN & Core) on **Kubernetes**, with an emphasis on **reliability, observability, GitOps, and automation**.

It is designed both as:
- A **hands-on lab** for practicing cloud-native SRE practices.
- A **portfolio project** to showcase expertise in Kubernetes, AWS, OpenShift, and DevOps.

---

## 🎯 Project Goals
- Simulate **RAN (Radio Access Network)** and **Core Network** workloads with lightweight FastAPI apps.
- Operate them reliably on **Kubernetes (local & AWS EKS)**.
- Implement **SRE principles**: SLIs, SLOs, error budgets, burn-rate alerts, and RCAs.
- Demonstrate **observability & incident response** with Prometheus, Grafana, and chaos drills.
- Showcase **GitOps deployments** with Argo CD (app-of-apps pattern).
- Provide **multi-cloud flavor**: AWS (EKS) and OpenShift (routes, Tekton pipelines).

---

## 🛠️ Technology Stack

### Infrastructure
- **WSL2 + Docker Desktop** → Local development environment  
- **k3d** → Local Kubernetes cluster for dev/test  
- **AWS EKS + Terraform** → Production-like environment in AWS  
- **OpenShift (OCP/OKD)** → Optional enterprise Kubernetes flavor  

### Application Layer
- **FastAPI (Python)** → RAN & Core simulators  
- **Docker** → Containerization  
- **Helm & Kustomize** → Deployment and configuration management  

### Observability & SRE
- **Prometheus** → Metrics collection  
- **Grafana** → Dashboards (RAN, Core, SLO budgets)  
- **Alertmanager** → SLO-based alerting  
- **Blackbox Exporter** → Synthetic probes (availability SLIs)  
- **k6** → Synthetic load testing  
- **Custom PrometheusRules** → Error budget burn rate, latency alerts  

### CI/CD & GitOps
- **GitLab CI/CD** → Build, push, and deploy pipelines  
- **Argo CD (App-of-Apps)** → GitOps deployment management  
- **Tekton Pipelines** (OpenShift option) → Alternative CI/CD  

### Reliability & Security
- **Chaos scripts** → Pod kill drills for incident simulation  
- **RCA templates** → Root cause analysis documentation  
- **NetworkPolicy, SecurityContext** → Restrictive defaults  
- **Storage** → Longhorn (local), Robin.io / AWS gp3 (cloud/OpenShift)  

---

## 🏗️ Architecture Diagram

```mermaid
graph TD
    subgraph Local Dev (WSL2 + k3d)
        A1[RAN Simulator (FastAPI)]
        A2[Core Simulator (FastAPI)]
        A3[Prometheus + Grafana]
        A4[Argo CD]
    end

    subgraph Cloud (AWS EKS / OpenShift)
        B1[RAN Simulator (FastAPI, ECR Image)]
        B2[Core Simulator (FastAPI, ECR Image)]
        B3[Prometheus Operator]
        B4[Grafana Dashboards]
        B5[Argo CD App-of-Apps]
        B6[Alertmanager + BlackBox]
    end

    Dev[Developer Laptop] --> Local
    Local --> Cloud
    Cloud --> B1
    Cloud --> B2

    B1 --> B3[Metrics]
    B2 --> B3[Metrics]
    B3 --> B4[Grafana Dashboards]
    B6 --> Oncall[On-call Engineer]

    style Dev fill:#f7e5,stroke:#333
    style Local fill:#eef,stroke:#333
    style Cloud fill:#eef,stroke:#333
```

---

## 🚀 How to Run

### Local (WSL2 + k3d)
```bash
./local_dev.sh
# port-forward Grafana
kubectl -n platform port-forward svc/kube-prometheus-grafana 3000:80
# open http://localhost:3000
```

### Push Images to AWS ECR
```bash
./aws_push_ecr.sh us-east-1
```

### Provision EKS + Deploy Apps
```bash
./eks_deploy.sh us-east-1 telco-eks
```

### OpenShift (Optional)
Follow [openshift/README-stepbystep.md](openshift/README-stepbystep.md)

---

## 📊 SRE Features
- **SLIs & SLOs** for availability, latency, error rate.  
- **PrometheusRules** for burn-rate detection.  
- **Grafana dashboards** for RAN, Core, and error budgets.  
- **Chaos drills** with `scripts/chaos/pod-kill.sh`.  
- **RCA templates** under `docs/rca/`.  

---

## 📜 License
MIT – free to use for learning and portfolio.
