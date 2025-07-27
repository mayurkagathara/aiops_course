"""
Classification EDA Script
Loads Breast Cancer dataset, performs basic EDA, and prepares train-test split.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

# 1️⃣ Load dataset
data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target, name="target")

print("Dataset shape:", X.shape)
print("Target classes:", data.target_names)

# 2️⃣ Basic EDA
print("\nSummary statistics:")
print(X.describe().T.head())

# Check class balance
sns.countplot(x=y)
plt.title("Class Balance")
plt.savefig("class_balance.png")
plt.show()

# Correlation heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(X.corr(), cmap="coolwarm", cbar=False)
plt.title("Feature Correlation Heatmap")
plt.savefig("Feature_Correlation.png")
plt.show()

# 3️⃣ Train-Test Split (Stratified to maintain class ratio)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Train size:", X_train.shape, " Test size:", X_test.shape)

# Save split data for next script
X_train.to_csv("X_train.csv", index=False)
X_test.to_csv("X_test.csv", index=False)
y_train.to_csv("y_train.csv", index=False)
y_test.to_csv("y_test.csv", index=False)