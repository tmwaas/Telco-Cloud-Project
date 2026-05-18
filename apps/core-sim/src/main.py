from fastapi import FastAPI
import random
import time

from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, Gauge

app = FastAPI(title="CORE Simulator")

# ------------------------------------------------------------------------------
# Prometheus Metrics
# ------------------------------------------------------------------------------

# Total sessions created
CORE_SESSIONS_TOTAL = Counter(
    "core_sessions_total",
    "Total number of 5G Core sessions created"
)

# QoS profile tracking
CORE_SESSIONS_BY_QOS = Counter(
    "core_sessions_by_qos",
    "Count of sessions by QoS profile",
    ["qos"]
)

# Latency (e.g., session setup latency)
CORE_SESSION_LATENCY = Histogram(
    "core_session_latency_ms",
    "Latency of core session creation (ms)",
    buckets=(5, 10, 25, 50, 75, 100, 200, 500)
)

# Current active sessions (gauge)
CORE_ACTIVE_SESSIONS = Gauge(
    "core_active_sessions",
    "Current active 5G core sessions"
)

# ------------------------------------------------------------------------------
# Initialize Instrumentator BEFORE app starts
# ------------------------------------------------------------------------------
instrumentator = Instrumentator().instrument(app).expose(app)

# ------------------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok", "component": "core"}


@app.get("/session")
def create_session():
    """
    Simulates 5G Core Session Establishment
    """
    start = time.time()

    # generate random QoS profile
    qos_profile = random.choice(["qci1", "qci5", "qci7", "qci9"])

    # simulate session latency
    latency_ms = random.randint(10, 200)

    # update metrics
    CORE_SESSIONS_TOTAL.inc()
    CORE_SESSIONS_BY_QOS.labels(qos=qos_profile).inc()
    CORE_SESSION_LATENCY.observe(latency_ms)
    CORE_ACTIVE_SESSIONS.inc()

    return {
        "status": "session_created",
        "qos": qos_profile,
        "latency_ms": latency_ms,
        "timestamp": time.time(),
    }


@app.get("/session/end")
def end_session():
    """
    Ends a random session (decrement gauge)
    """
    if CORE_ACTIVE_SESSIONS._value.get() > 0:
        CORE_ACTIVE_SESSIONS.dec()

    return {"status": "session_ended"}

