from fastapi import FastAPI
import random
import time
import requests
import os
import threading
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Gauge, Histogram

app = FastAPI(title="RAN Simulator")

# Prometheus metrics
RAN_UE_ATTACHED = Gauge(
    "ran_kpi_ue_attached_total", 
    "Total number of UEs currently attached to this RAN simulator"
)

RAN_RSRP_DBM = Gauge(
    "ran_kpi_rsrp_dbm", "Reference Signal Received Power (RSRP) in dBm"
)

RAN_SINR_DB = Gauge(
    "ran_kpi_sinr_db", "Signal to Interference plus Noise Ratio (SINR) in dB"
)

RAN_THROUGHPUT_MBPS = Gauge(
    "ran_kpi_throughput_mbps", "Downlink throughput in Mbps"
)

RAN_REQUEST_LATENCY = Histogram(
    "ran_request_latency_seconds",
    "Latency of RAN KPI requests",
    buckets=(0.01, 0.05, 0.1, 0.2, 0.5, 1, 2),
)

# Initialize Metrics
RAN_UE_ATTACHED.set(0)
RAN_RSRP_DBM.set(-110)
RAN_SINR_DB.set(0)
RAN_THROUGHPUT_MBPS.set(0)

# Set default to root URL if /health doesn't exist on core-sim
CORE_URL = os.getenv("CORE_URL", "http://core-sim:80/")

def signaling_worker():
    """Background thread simulating 5G Control Plane signaling (N2/N3 interface simulation)"""
    print(f"Starting 5G Signaling worker to {CORE_URL}...")
    while True:
        try:
            # Simulating heartbeat signaling to the Core Network
            response = requests.get(CORE_URL, timeout=5)
            # Safe logging: using status_code instead of .json() to avoid crash
            if response.status_code == 200:
                print(f"[SIGNALING] Heartbeat to Core Success: {response.status_code}")
            else:
                print(f"[SIGNALING] Core returned status: {response.status_code}")
        except Exception as e:
            print(f"[SIGNALING] Connection to Core failed: {e}")
        
        time.sleep(10)

# Start signaling thread
threading.Thread(target=signaling_worker, daemon=True).start()        

# Instrument the app for Prometheus
instrumentator = Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health():
    return {"status": "ok", "component": "ran"}

@app.get("/kpi")
def kpi():
    """Endpoint to fetch and update RAN Key Performance Indicators"""
    start = time.time()

    # Simulate dynamic UE behavior
    current_ues = random.randint(5, 45)
    RAN_UE_ATTACHED.set(current_ues)

    # Simulate Radio conditions
    rsrp = random.randint(-120, -80)
    sinr = round(random.uniform(0, 20), 2)
    throughput = round(random.uniform(10, 300), 2)

    # Update Prometheus metrics
    RAN_RSRP_DBM.set(rsrp)
    RAN_SINR_DB.set(sinr)
    RAN_THROUGHPUT_MBPS.set(throughput)

    # Record Latency
    RAN_REQUEST_LATENCY.observe(time.time() - start)

    return {
        "rsrp": rsrp,
        "sinr": sinr,
        "throughput_mbps": throughput,
        "attached_ues": current_ues,
        "timestamp": time.time(),
    }