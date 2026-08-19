from prometheus_client import Counter, Histogram, Gauge, start_http_server
from config.settings import get_settings


rounds_collected_total = Counter("rounds_collected_total", "Total rounds collected across all sources")
prediction_requests_total = Counter("prediction_requests_total", "Total prediction requests served")
prediction_latency_seconds = Histogram("prediction_latency_seconds", "Latency of prediction models")
active_models_gauge = Gauge("active_models_count", "Number of active analytical models")
system_cpu_usage = Gauge("system_cpu_usage_percent", "System CPU usage percentage")
system_memory_usage = Gauge("system_memory_usage_percent", "System memory usage percentage")


def start_metrics_server():
    settings = get_settings()
    start_http_server(settings.prometheus_port)
