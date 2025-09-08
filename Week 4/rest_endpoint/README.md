# AIOps Alerts API (FastAPI)

This project implements a **FastAPI-based REST API** for ingesting and managing alerts in an AIOps-like system, inspired by platforms like BigPanda.

---

## Features

- **API Key Authentication** (`X-API-Key` header)
- **JSON Payload Validation**
  - Requires `identifier` and `host` fields
- **Rate Limiting**
  - Max **5 alerts/minute** (excess stored in `alert_storm.json`)
- **Deduplication**
  - Based on `identifier` field (updates existing alert if duplicate)
- **Host Suppression**
  - More than **3 alerts/host/minute** → host suppressed for next 60s
- **File-based Storage**
  - Active alerts → `alerts.json`
  - Rate-limited alerts → `alert_storm.json`
  - Suppressed alerts → `suppressed.json`

---

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn

Install dependencies:

```bash
pip install fastapi uvicorn
```

---

## Running the API

1. Save the Python code as `main.py`.
2. Start the server:

    ```bash
    uvicorn main:app --reload
    ```

3. The API will be available at:

    ```text
    http://127.0.0.1:8000
    ```

---

## API Usage ([Swagger](http://localhost:8000/docs))

### Endpoint

**POST** `/alerts`

#### Headers

```sh
Content-Type: application/json
X-API-Key: MY_SECURE_API_KEY
```

#### Example Payload

```json
{
"identifier": "alert123",
"host": "server1",
"message": "CPU usage high"
}
```

---

## Alert Processing Flow

1. **Authentication** — rejects invalid API key.
2. **Validation** — checks for `identifier` and `host` fields.
3. **Host Suppression** — if host exceeded threshold, alert stored in `suppressed.json`.
4. **Rate Limiting** — if overall limit exceeded, alert stored in `alert_storm.json`.
5. **Deduplication** — if identifier exists, alert updated in `alerts.json`; else added.
6. **Metadata** — `received_at` and `source_ip` fields added before saving.

---

## File Outputs

- `alerts.json` — active, deduplicated alerts.
- `alert_storm.json` — rate-limited alerts.
- `suppressed.json` — suppressed alerts.

---

## Running Tests

**Bash test script** is provided: `test_alerts_api.sh`

1. Ensure the API is running

    ```bash
    uvicorn main:app --reload
    ```

2. Make the script executable:

    ```bash
    chmod +x test_alerts_api.sh
    ```

3. Run tests:

    ```bash
    ./test_alerts_api.sh
    ```

4. The script will:

   - Send alerts for all scenarios (valid, duplicate, missing fields, invalid key, rate limiting, suppression, invalid JSON)
   - Print **PASS/FAIL** results in color

---

## Example Test Output

```sh
=== Running API Tests ===
TEST: Valid alert ... PASS
TEST: Duplicate identifier (update) ... PASS
TEST: Missing identifier ... PASS
TEST: Missing host ... PASS
TEST: Invalid API Key ... PASS
TEST: Rate limit exceeded (6th alert) ... PASS
TEST: Host suppression (4th alert from same host) ... PASS
TEST: Host still suppressed ... PASS
TEST: Invalid JSON ... PASS

PASS: 9  FAIL: 0
```

---

## Notes

- Rate limit & suppression timers reset after 60 seconds.
- All data is stored locally; in production, use a database or caching layer (Redis, PostgreSQL, etc.).
- The API Key can be changed in `main.py`.

---
