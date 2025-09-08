from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import uvicorn

# Load model and scaler
model = joblib.load("anomaly_model.pkl")
scaler = joblib.load("scaler.pkl")

app = FastAPI(title="System Metrics Anomaly Detection API")

class MetricsInput(BaseModel):
    cpu: float
    ram: float
    net_sent: float
    net_recv: float

@app.post("/detect")
def detect_anomaly(data: MetricsInput):
    X_new = np.array([[data.cpu, data.ram, data.net_sent, data.net_recv]])
    X_scaled = scaler.transform(X_new)

    pred = model.predict(X_scaled)  # -1 = anomaly, 1 = normal
    score = model.decision_function(X_scaled)[0]  # lower = more anomalous

    return {
        "anomaly": bool(pred[0] == -1),
        "score": float(score)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
