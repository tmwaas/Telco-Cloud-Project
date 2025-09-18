from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import random, time

app = FastAPI(title="core-sim")
REQS = Counter("core_requests_total","Total requests",["ep","code"])
LAT = Histogram("http_request_duration_seconds","latency",buckets=(0.02,0.05,0.1,0.2,0.5,1,2))

@app.get("/healthz")
def health(): REQS.labels("healthz","200").inc(); return {"ok":True}

@app.post("/session/create")
def create():
    with LAT.time(): time.sleep(random.uniform(0.03,0.12))
    REQS.labels("create","200").inc()
    return {"session":"created"}

@app.post("/session/terminate")
def term():
    with LAT.time(): time.sleep(random.uniform(0.02,0.08))
    REQS.labels("terminate","200").inc()
    return {"session":"terminated"}

@app.get("/metrics")
def metrics(): return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
