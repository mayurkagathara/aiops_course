from fastapi import FastAPI
from pydantic import BaseModel
from rabbitmq_client import RabbitMQClient

app = FastAPI()
rabbitmq_client = RabbitMQClient()

# Pydantic models for incoming alerts
class RestAlert(BaseModel):
    # Your REST alert model
    source: str = "rest"
    host: str
    message: str
    severity: str

class GrafanaAlert(BaseModel):
    # Your Grafana alert model
    source: str = "grafana"
    host: str
    description: str
    level: str   

@app.get("/")
async def greet():
    return "Hello, I am FastAPI.."

@app.post("/alerts/rest")
async def receive_rest_alert(alert: RestAlert):
    # Publish to RabbitMQ with the 'rest' routing key
    rabbitmq_client.publish_alert("rest", alert.model_dump())
    return {"status": "Alert accepted"}

@app.post("/alerts/grafana")
async def receive_grafana_alert(alert: GrafanaAlert):
    # Publish to RabbitMQ with the 'grafana' routing key
    rabbitmq_client.publish_alert("grafana", alert.model_dump())
    return {"status": "Alert accepted"}

@app.post("/alerts/grafanav2")
async def receive_grafana_alert(alert: dict):
    # Publish to RabbitMQ with the 'grafanav2' routing key
    rabbitmq_client.publish_alert("grafanav2", alert)
    return {"status": "Alert accepted"}