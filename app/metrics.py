from prometheus_client import Counter, Histogram

# HTTP Metrics
REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "http_status"]
)
REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds", "Latency of HTTP requests", ["method", "endpoint"]
)

# Feature-Specific Metrics
INCIDENTS_CREATED = Counter("incidents_created_total", "Total number of incidents created")