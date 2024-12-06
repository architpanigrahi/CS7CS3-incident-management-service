from fastapi import Request
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter('request_count', 'Application Request Count', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency', ['method', 'endpoint'])

async def metrics_middleware(request: Request, call_next):
    method = request.method
    endpoint = request.url.path
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
    with REQUEST_LATENCY.labels(method=method, endpoint=endpoint).time():
        response = await call_next(request)
    return response