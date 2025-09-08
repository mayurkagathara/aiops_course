# Week 4: AIOps Alert Processing and Monitoring Pipeline

This week's modules demonstrate a comprehensive AIOps pipeline implementation focusing on alert processing, monitoring, and visualization. The project is split into three main components:

## 📁 Project Structure

```sh
Week 4/
├── AIOPS_APPLICATION_REST/       # Alert Processing Application
│   ├── Alert_Processing_Service/ # Backend Alert Processing
│   └── REST_endpoint/           # FastAPI REST API
├── aiops-demo/                  # Monitoring Pipeline
│   ├── prometheus/             # Metrics Collection
│   ├── alertmanager/          # Alert Management
│   └── otel-collector/        # OpenTelemetry Collection
└── rest_endpoint/             # Standalone Alert API Demo
```

## 🔍 Module Overview

### 1. AIOPS_APPLICATION_REST

A complete alert processing application with two main components:

#### REST Endpoint (FastAPI)

- Receives alerts from multiple sources (REST, Grafana)
- Uses RabbitMQ for message queuing
- Implements async processing with FastAPI
- Supports different alert formats and routing

#### Alert Processing Service

- Processes alerts from RabbitMQ queue
- Enriches alerts with additional data
- Maintains maintenance window awareness
- Stores processed alerts in SQLite database
- Supports CSV-based enrichment data

### 2. aiops-demo

An end-to-end AIOps monitoring pipeline using Docker:

- **OpenTelemetry Collector**: Metrics collection
- **Prometheus**: Metrics storage and querying
- **Grafana**: Visualization dashboards
- **Alertmanager**: Alert routing and management

Key Features:

- Windows-friendly configuration
- Docker Compose orchestration
- Pre-configured monitoring stack
- Ready-to-use dashboards

### 3. rest_endpoint

A standalone alert API demonstration:

- FastAPI-based REST API
- Advanced alert management features:
  - API Key authentication
  - Rate limiting (5 alerts/minute)
  - Alert deduplication
  - Host-based suppression
  - JSON-based storage

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Docker Desktop (for aiops-demo)
- RabbitMQ (for AIOPS_APPLICATION_REST)

### Running the Projects

#### AIOPS_APPLICATION_REST

##### 1. Start the REST endpoint

```bash
cd AIOPS_APPLICATION_REST/REST_endpoint
python -m uvicorn main:app --reload
```

##### 2. Start the Alert Processing Service

```bash
cd AIOPS_APPLICATION_REST/Alert_Processing_Service
python alert_processor.py
```

#### aiops-demo

```bash
cd aiops-demo
docker-compose up --build -d
```

#### rest_endpoint

```bash
cd rest_endpoint
uvicorn fast_rest_endpoint:app --reload
```

## 📊 Key Features Across Modules

1. **Alert Processing**
   - Multiple input sources
   - Message queue integration
   - Alert enrichment
   - Maintenance window awareness

2. **Monitoring**
   - Metric collection
   - Data visualization
   - Alert management
   - Container orchestration

3. **API Features**
   - Authentication
   - Rate limiting
   - Deduplication
   - Alert suppression

## 🔗 Dependencies

- FastAPI
- Pydantic
- RabbitMQ
- SQLite
- Docker
- OpenTelemetry
- Prometheus
- Grafana
- Alertmanager

## 📝 Notes

- Each module can be run independently
- The aiops-demo is specifically designed to be Windows-friendly
- Configuration files are provided for all components
- Sample data and test scripts are included
- All modules follow best practices for AIOps implementations
