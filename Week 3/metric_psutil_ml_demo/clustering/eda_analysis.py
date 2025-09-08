import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

JSON_FILE = "system_metrics.json"

# Load JSON into DataFrame
with open(JSON_FILE, "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)
print(df.head())
print(df.describe())

# Correlation heatmap
plt.figure(figsize=(8, 5))
sns.heatmap(df[["cpu","ram","disk","net_sent","net_recv"]].corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.savefig("haetmap.png")
plt.show()

# Pairplot
sns.pairplot(df, vars=["cpu","ram","disk","net_sent","net_recv"])
plt.savefig("pairplot.png")
plt.show()
