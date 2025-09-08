from fastapi import FastAPI
import joblib
from pydantic import BaseModel
import uvicorn

# Load trained model and scaler
model = joblib.load("kmeans_model.pkl")
scaler = joblib.load("scaler.pkl")

app = FastAPI(title="System Metrics Clustering API")

class InputData(BaseModel):
    cpu: float
    ram: float
    disk: float
    net_sent: float
    net_recv: float

@app.post("/predict")
def predict_cluster(data: InputData):
    X = [[data.cpu, data.ram, data.disk, data.net_sent, data.net_recv]]
    X_scaled = scaler.transform(X)
    cluster = int(model.predict(X_scaled)[0])
    return {"assigned_cluster": cluster}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

## with defined cluster name 
# from fastapi import FastAPI
# import joblib
# from pydantic import BaseModel
# import uvicorn
# import numpy as np

# # Load saved model, scaler, and cluster labels
# model = joblib.load("best_cluster_model.pkl")
# scaler = joblib.load("scaler.pkl")
# cluster_labels = joblib.load("cluster_labels.pkl")

# app = FastAPI(title="System Metrics Clustering API")

# class InputData(BaseModel):
#     cpu: float
#     ram: float
#     disk: float
#     net_sent: float
#     net_recv: float

# @app.post("/predict")
# def predict_cluster(data: InputData):
#     X_new = np.array([[data.cpu, data.ram, data.disk, data.net_sent, data.net_recv]])
#     X_scaled = scaler.transform(X_new)

#     # Some clustering models (like Agglomerative) do not support predict()
#     if hasattr(model, "predict"):
#         cluster = int(model.predict(X_scaled)[0])
#     else:
#         # Workaround for models without predict(): fit to existing + new input
#         combined = np.vstack([scaler.transform(X_new)])  # only new input
#         cluster = int(model.fit_predict(combined)[0])

#     meaning = cluster_labels.get(cluster, "Unknown")

#     return {"cluster": cluster, "meaning": meaning}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
