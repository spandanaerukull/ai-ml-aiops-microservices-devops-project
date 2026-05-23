import time
import statistics
import requests
from prometheus_client import Gauge, start_http_server

PROMETHEUS_URL = "http://monitoring-kube-prometheus-prometheus.monitoring.svc.cluster.local:9090"

CPU_QUERY = 'sum(rate(container_cpu_usage_seconds_total{namespace="default", container!="", pod!=""}[2m])) by (pod)'

aiops_pod_cpu_usage = Gauge(
    "aiops_pod_cpu_usage",
    "CPU usage detected by AIOps anomaly detector",
    ["pod"]
)

aiops_pod_anomaly = Gauge(
    "aiops_pod_anomaly",
    "AI anomaly detection result for Kubernetes pods. 1 means anomaly, 0 means normal",
    ["pod"]
)


def collect_metrics():
    try:
        response = requests.get(
            f"{PROMETHEUS_URL}/api/v1/query",
            params={"query": CPU_QUERY},
            timeout=10
        )
        response.raise_for_status()

        data = response.json()["data"]["result"]

        values = []
        for item in data:
            pod = item["metric"].get("pod", "unknown")
            value = float(item["value"][1])
            values.append((pod, value))

        print("\nAIOps CPU Anomaly Report")
        print("------------------------")

        if not values:
            print("No metrics found from Prometheus")
            return

        cpu_values = [value for _, value in values]
        avg_cpu = statistics.mean(cpu_values)

        for pod, value in values:
            aiops_pod_cpu_usage.labels(pod=pod).set(value)

            if avg_cpu > 0 and value > avg_cpu * 2:
                aiops_pod_anomaly.labels(pod=pod).set(1)
                print(f"ANOMALY: {pod} high CPU usage: {value}")
            else:
                aiops_pod_anomaly.labels(pod=pod).set(0)
                print(f"OK: {pod} CPU usage: {value}")

    except Exception as error:
        print(f"ERROR: Failed to collect/analyze metrics: {error}")


if __name__ == "__main__":
    print("Starting AIOps Anomaly Detector...")
    print("Metrics endpoint started on port 8000")

    start_http_server(8000)

    while True:
        collect_metrics()
        time.sleep(60)