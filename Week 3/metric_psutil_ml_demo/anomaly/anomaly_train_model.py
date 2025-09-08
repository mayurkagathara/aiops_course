import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor

JSON_FILE = "system_metrics.json"

# Load JSON Data
with open(JSON_FILE, "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)
X = df[["cpu", "ram", "net_sent", "net_recv"]]

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Define models
models = {
    "IsolationForest": IsolationForest(contamination=0.1, random_state=42),
    "OneClassSVM": OneClassSVM(kernel="rbf", nu=0.1, gamma="scale"),
    "LOF": LocalOutlierFactor(n_neighbors=20, contamination=0.1)
}

results = {}

# Train & Predict anomalies
for name, model in models.items():
    if name == "LOF":  # LOF has no separate fit/predict
        preds = model.fit_predict(X_scaled)
    else:
        model.fit(X_scaled)
        preds = model.predict(X_scaled)

    preds = np.where(preds == -1, 1, 0)  # 1 = anomaly, 0 = normal
    results[name] = {"model": model, "preds": preds}
    print(f"{name} → Detected {sum(preds)} anomalies out of {len(preds)}")

# Pick Isolation Forest as final model
final_model = results["IsolationForest"]["model"]
df["anomaly"] = results["IsolationForest"]["preds"]

# Save model & scaler
joblib.dump(final_model, "anomaly_model.pkl")
joblib.dump(scaler, "scaler.pkl")
print("✅ Saved Isolation Forest Model as anomaly_model.pkl")

# -------------------------------------------------
# 1️⃣ Scatter Plot (CPU vs RAM) with anomalies
# -------------------------------------------------
plt.figure(figsize=(7, 5))
sns.scatterplot(
    x=df["timestamp"], y=df["ram"], hue=df["anomaly"], palette={0: "green", 1: "red"}, s=60
)
plt.title("Anomalies (CPU vs RAM)")
plt.xlabel("CPU Usage (%)")
plt.ylabel("RAM Usage (%)")
plt.legend(title="Anomaly", labels=["Normal", "Anomaly"])
plt.show()

# -------------------------------------------------
# 2️⃣ Subplot for All Metrics (Color-coded by anomaly)
# -------------------------------------------------
metrics = ["cpu", "ram", "net_sent", "net_recv"]
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes = axes.flatten()

colors = df["anomaly"].map({0: "green", 1: "red"})

for i, metric in enumerate(metrics):
    axes[i].scatter(range(len(df)), df[metric], c=colors, s=40)
    axes[i].set_title(metric)
    axes[i].set_xlabel("Index")
    axes[i].set_ylabel(metric)

plt.suptitle("Metrics with Anomalies Highlighted", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
