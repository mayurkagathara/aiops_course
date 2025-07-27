import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

X = pd.read_csv("X_cluster.csv")

# Elbow Method for KMeans
inertia = []
for k in range(2, 8):
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(X)
    inertia.append(km.inertia_)

plt.plot(range(2, 8), inertia, marker="o")
plt.title("Elbow Method")
plt.xlabel("k")
plt.ylabel("Inertia")
plt.savefig("elbow_plot.png")
plt.show()

# Train final models
km = KMeans(n_clusters=3, random_state=42).fit(X)
hc = AgglomerativeClustering(n_clusters=3).fit(X)

print("KMeans Silhouette:", silhouette_score(X, km.labels_))
print("Agglomerative Silhouette:", silhouette_score(X, hc.labels_))