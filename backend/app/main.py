from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Education Cluster API")

# Setup Prometheus Monitoring (Sesuai Dokumen Poin 4.4)
Instrumentator().instrument(app).expose(app)

@app.get("/")
def read_root():
    return {"status": "active", "service": "MLOps Backend API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}