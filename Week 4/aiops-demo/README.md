# 📊 AIOps Demo Pipeline (Windows-friendly)

This project demonstrates an **end-to-end AIOps pipeline** using:

* **OpenTelemetry Collector (OTEL)** → collects metrics
* **Prometheus** → scrapes metrics
* **Grafana** → visualization dashboards
* **Alertmanager** → sends alerts to REST API endpoint

This version is **Windows-friendly** because all configuration files are baked into Docker images (no volume mounts).

---

## 🚀 Prerequisites

* **Windows 11**
* **Docker Desktop** installed and running
* **Docker Compose v2+**

---

## 📂 Folder Structure

```sh
aiops-demo/
├── docker-compose.yml
├── prometheus/
│   ├── Dockerfile
│   └── prometheus.yml
├── alertmanager/
│   ├── Dockerfile
│   └── alertmanager.yml
├── otel-collector/
│   ├── Dockerfile
│   └── otel-config.yml
```

---

## ▶️ How to Run

1. Open **PowerShell** in the `aiops-demo/` folder.

2. Build and start all services:

   ```powershell
   docker-compose up --build -d
   ```

3. Verify containers are running:

   ```powershell
   docker ps
   ```

4. Access services:

   * Grafana → [http://localhost:3000](http://localhost:3000) (login: `admin/admin`)
   * Prometheus → [http://localhost:9090](http://localhost:9090)
   * Alertmanager → [http://localhost:9093](http://localhost:9093)

---

## 📊 Grafana Setup

1. Login with `admin / admin`.
2. Add Prometheus as a data source:

   * Go to **Connections → Data sources → Add data source → Prometheus**
   * URL: `http://prometheus:9090`
   * Save & Test
3. Import a sample dashboard:

   * Go to **Dashboards → New → Import**
   * Paste **Dashboard ID: 1860** (Node Exporter Full) or create a custom one.

---

## ⚠️ Alert Rules Setup

### 1. Create a Prometheus Alert Rule (inside `prometheus.yml`)

Example rule (already baked in):

```yaml
rule_files:
  - /etc/prometheus/alerts.yml
```

Where `alerts.yml` could look like:

```yaml
groups:
  - name: example
    rules:
      - alert: HighCPUUsage
        expr: process_cpu_seconds_total > 0.5
        for: 10s
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"
```

(extend as needed)

### 2. Alertmanager Receiver

`alertmanager.yml` is configured to send alerts to your REST API endpoint:

```yaml
route:
  receiver: "default-receiver"

receivers:
  - name: "default-receiver"
    webhook_configs:
      - url: "http://host.docker.internal:8080/alert"
```

This means alerts will be POSTed to your local service at `http://localhost:8080/alert`.

---

## 🛠️ Stopping Services

```powershell
docker-compose down
```

---

## 📌 Next Steps

* Add **custom dashboards** in Grafana.
* Write a **REST API service** to handle alerts (e.g., FastAPI, Flask).
* Later, integrate **ML anomaly detection** before sending alerts.

---

✅ This stack should now start cleanly on **Windows 11** with:

```powershell
docker-compose up --build -d
```
