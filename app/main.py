from fastapi import FastAPI
from prometheus_client import make_asgi_app
from prometheus_fastapi_instrumentator import Instrumentator

from app.router import incident_router
from app.monitoring import metrics_middleware
from app.router.incident_router import router as incident_router

# app = FastAPI()
#
# # Include routers
# app.include_router(incident_router.router)
#
# # Add Prometheus monitoring
# app.middleware('http')(metrics_middleware)
#
# # Prometheus metrics endpoint
# app.mount("/metrics", make_asgi_app())

app = FastAPI(
    title="Incident Management Service",
    description="A service for managing incidents such as fire, flood, and other emergencies.",
    version="1.0.0"
)

instrumentator = Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Include the incident router
app.include_router(incident_router, prefix="/api", tags=["Incidents"])

# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    """
    Check if the service is running and healthy.

    Returns:
        dict: A JSON response indicating service health.
    """
    return {"status": "OK"}