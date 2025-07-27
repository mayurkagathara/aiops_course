"""
Regression EDA using Diabetes dataset.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

data = load_diabetes()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target, name="target")

print("Dataset shape:", X.shape)
print("Target stats:\n", y.describe())

# Pairplot for first few features
sns.pairplot(pd.concat([X.iloc[:, :4], y], axis=1))
plt.savefig("pairplot.png")
plt.show()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train.to_csv("X_train_reg.csv", index=False)
X_test.to_csv("X_test_reg.csv", index=False)
y_train.to_csv("y_train_reg.csv", index=False)
y_test.to_csv("y_test_reg.csv", index=False)