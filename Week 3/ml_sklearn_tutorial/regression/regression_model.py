import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

X_train = pd.read_csv("X_train_reg.csv")
X_test = pd.read_csv("X_test_reg.csv")
y_train = pd.read_csv("y_train_reg.csv").values.ravel()
y_test = pd.read_csv("y_test_reg.csv").values.ravel()

models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1.0)
}

cv = KFold(n_splits=5, shuffle=True, random_state=42)

for name, model in models.items():
    print(f"\n🔹 Training {name}")
    scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="r2")
    print("Mean CV R²:", scores.mean())

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("Test R²:", r2_score(y_test, y_pred))
    print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))


from lazypredict.Supervised import LazyRegressor
reg = LazyRegressor(verbose=0,
                    ignore_warnings=False,
                    custom_metric=None)

models, predictions = reg.fit(X_train, X_test, y_train, y_test)
print(models)
