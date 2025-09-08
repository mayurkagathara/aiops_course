import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.decomposition import PCA
import joblib
import numpy as np

JSON_FILE = "system_metrics.json"

# Load data
with open(JSON_FILE, "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)
X = df[["cpu", "ram", "disk", "net_sent", "net_recv"]]

# -------------------------------
# Standardization
# -------------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -------------------------------
# Elbow Method for KMeans
# -------------------------------
inertias = []
K_range = range(2, 8)

for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

plt.figure(figsize=(6, 4))
plt.plot(K_range, inertias, marker="o")
plt.title("Elbow Method for Optimal k (KMeans)")
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Inertia (WCSS)")
plt.show()

optimal_k = 3  # You can pick based on the elbow curve

# -------------------------------
# Try Multiple Models
# -------------------------------
models = {
    "KMeans": KMeans(n_clusters=optimal_k, random_state=42, n_init=10),
    "Agglomerative": AgglomerativeClustering(n_clusters=optimal_k),
    "DBSCAN": DBSCAN(eps=1.5, min_samples=3),
}

results = []

for name, model in models.items():
    labels = model.fit_predict(X_scaled)

    if len(set(labels)) > 1:
        sil = silhouette_score(X_scaled, labels)
        db = davies_bouldin_score(X_scaled, labels)
    else:
        sil, db = -1, 999  # Poor scores if only 1 cluster

    results.append(
        {"model": name, "object": model, "labels": labels, "silhouette": sil, "davies_bouldin": db}
    )

# -------------------------------
# Pick Best Model (High Silhouette, Low DB)
# -------------------------------
best_model = sorted(results, key=lambda x: (-x["silhouette"], x["davies_bouldin"]))[0]

print("\n🔹 Model Comparison:")
for r in results:
    print(f"{r['model']}: clusters={len(set(r['labels']))}, silhouette={r['silhouette']:.3f}, db={r['davies_bouldin']:.3f}")

print(f"\n✅ Best Model Selected: {best_model['model']}")

# # Compute cluster meaning based on avg CPU & RAM
# cluster_stats = pd.DataFrame({"cluster": best_model["labels"]})
# cluster_stats["cpu"] = X["cpu"]
# cluster_stats["ram"] = X["ram"]

# cluster_means = cluster_stats.groupby("cluster")[["cpu", "ram"]].mean()

# cluster_labels = {}
# sorted_clusters = cluster_means.sort_values(["cpu", "ram"], ascending=True).index.tolist()

# for i, cluster in enumerate(sorted_clusters):
#     if i == 0:
#         cluster_labels[int(cluster)] = "Idle"
#     elif i == 1:
#         cluster_labels[int(cluster)] = "Moderate Load"
#     else:
#         cluster_labels[int(cluster)] = "High Load"

# print("\nCluster Labels Mapping:", cluster_labels)

# # Save model, scaler, and cluster labels
# joblib.dump(scaler, "scaler.pkl")
# joblib.dump(best_model["object"], "best_cluster_model.pkl")
# joblib.dump(cluster_labels, "cluster_labels.pkl")

# print("✅ Model, Scaler, and Cluster Labels saved!")



# -------------------------------
# Save Best Model + Scaler
# -------------------------------
joblib.dump(scaler, "scaler.pkl")
joblib.dump(best_model["object"], "best_cluster_model.pkl")
print("Model saved as best_cluster_model.pkl and scaler.pkl")

# -------------------------------
# PCA for Visualization
# -------------------------------
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
df_pca = pd.DataFrame(X_pca, columns=["PC1", "PC2"])
df_pca["cluster"] = best_model["labels"]

plt.figure(figsize=(7, 5))
plt.scatter(df_pca["PC1"], df_pca["PC2"], c=df_pca["cluster"], cmap="viridis", s=60)
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title(f"Cluster Visualization (PCA 2D) - {best_model['model']}")
plt.colorbar(label="Cluster")
plt.show()
