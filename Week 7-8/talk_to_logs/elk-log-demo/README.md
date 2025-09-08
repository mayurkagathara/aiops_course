# ELK Log Demo (Windows-friendly)

Pipeline: **Python log generator → Logstash → Elasticsearch → Kibana** using Docker Desktop.

## Prerequisites

- Windows 11 with **Docker Desktop** installed and running.
- **Python 3.9+** in PATH (for the generator).

## Folder Layout

```sh
elk-log-demo/
├── docker-compose.yml
├── generate_logs.py
├── logs/
│   └── app.log           # generated
└── logstash/
    ├── pipeline/
    │   └── logstash.conf
    └── templates/
        └── logs-template.json
```

## 1) Start ELK stack

Open **PowerShell** in this folder and run:

```powershell
docker compose up -d
```

- Elasticsearch: <http://localhost:9200> (security disabled for local demo)
- Kibana: <http://localhost:5601>

> Tip: If Docker Desktop RAM is limited, adjust `ES_JAVA_OPTS` in `docker-compose.yml`.

## 2) Generate sample logs

Run the Python generator to create **1,00** lines:

```powershell
python .\generate_logs.py
```

This writes to `.\logs\app.log` which is mounted into the Logstash container at `/var/log/ingest/app.log`.

## 3) Ingest + parse with Logstash

Logstash tails `app.log` automatically. If you re-generate logs and they don't appear, you can reset sincedb:

```powershell
docker compose restart logstash
```

Or remove the sincedb file inside the container:

```powershell
docker exec -it $(docker ps -qf "name=logstash") powershell # or sh depending on image
```

(Then delete `/usr/share/logstash/sincedb/app.sincedb`)

## 4) Create Kibana index pattern

- Open Kibana → **Discover**.
- Create **Data View** with pattern: `logs-*` and time field `@timestamp`.
- Verify structured fields: `customer`, `customer_name`, `environment_name`, `application_name`, `log_level`, `log_type`, `message`.

## 5) Troubleshooting

- If Elasticsearch is "yellow" or "red", give Docker more resources or restart containers.
- If no logs appear, check Logstash logs:

  ```powershell
  docker compose logs -f logstash
  ```

- Ensure `logs/app.log` exists and has content.
- Windows file sharing must be enabled in Docker Desktop for your drive.
- If GROK fails, Logstash will tag events with `_grokparsefailure`; check patterns and sample lines.

## 6) Regenerating data

Run the generator again to overwrite `logs/app.log`:

```powershell
python .\generate_logs.py
```

## 7) Customization

- Edit `generate_logs.py` to change applications, customers, or message mix.
- Extend GROK to pull additional metrics (e.g., extract `duration_ms` from the message).
