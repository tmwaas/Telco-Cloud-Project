from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import random, time

app = FastAPI(title="ran-sim")
REQS = Counter("ran_requests_total", "Total requests", ["path","code"])
LAT = Histogram("http_request_duration_seconds","latency",buckets=(0.02,0.05,0.1,0.2,0.5,1,2))

@app.get("/healthz")
def health(): REQS.labels("/healthz","200").inc(); return {"ok":True}

@app.get("/uplink")
def up(): 
    with LAT.time(): time.sleep(random.uniform(0.03,0.12))
    REQS.labels("/uplink","200").inc()
    return {"status":"uplink-ok"}

@app.get("/downlink")
def down():
    with LAT.time(): time.sleep(random.uniform(0.03,0.12))
    REQS.labels("/downlink","200").inc()
    return {"status":"downlink-ok"}

@app.get("/metrics")
def metrics(): return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
