# 📘 Glossary of Terms (for all 3 problems)

This glossary explains **all jargon and technical terms** used in the code and README files.

---

## 📊 **Key Concepts in Machine Learning**

### 🔹 **Dataset**

A collection of features (input variables) and target (output variable).

### 🔹 **Feature (X)**

The input variables used to predict the target.

### 🔹 **Target (y)**

The output variable we are trying to predict (classification or regression).

### 🔹 **Train-Test Split**

Dividing the dataset into **training data** (to train the model) and **test data** (to evaluate performance).

### 🔹 **Stratified Train-Test Split**

Ensures that the proportion of classes in training and test sets remains the same as the original dataset.

### 🔹 **Cross-Validation (CV)**

Splits the dataset into multiple folds for training and validation to get more reliable performance estimates.

### 🔹 **KFold**

Cross-validation method that splits the data into K equally sized folds.

### 🔹 **StratifiedKFold**

A variant of KFold for classification problems that preserves class proportions in each fold.

---

## 🤖 **Machine Learning Algorithms Used**

### 🔹 **Logistic Regression**

A simple classification algorithm that predicts the probability of classes using a logistic (sigmoid) function.

### 🔹 **Random Forest**

An ensemble algorithm that combines multiple decision trees and averages their predictions for better accuracy.

### 🔹 **Linear Regression**

A regression algorithm that fits a straight line to predict continuous values.

### 🔹 **Ridge Regression**

A variant of linear regression with regularization to prevent overfitting.

### 🔹 **KMeans Clustering**

An unsupervised algorithm that partitions data into **k clusters** by minimizing intra-cluster distance.

### 🔹 **Agglomerative Clustering**

A hierarchical clustering algorithm that merges clusters iteratively based on similarity.

### 🔹 **PCA (Principal Component Analysis)**

A dimensionality reduction technique that projects high-dimensional data into fewer dimensions while preserving variance.

---

## 📈 **Metrics Used**

### 🔹 **Accuracy**

Percentage of correctly predicted samples:
$$ \text{Accuracy} = \frac{\text{Correct Predictions}}{\text{Total Samples}} $$

### 🔹 **Precision**

Out of all predicted positives, how many are correct:
$$ \text{Precision} = \frac{TP}{TP+FP} $$

### 🔹 **Recall (Sensitivity)**

Out of all actual positives, how many are correctly predicted:
$$ \text{Recall} = \frac{TP}{TP+FN} $$

### 🔹 **F1-Score**

Harmonic mean of Precision and Recall:
$$ F1 = 2 \times \frac{Precision \times Recall}{Precision + Recall} $$

### 🔹 **ROC-AUC Score**

Measures how well the model separates classes by plotting True Positive Rate vs False Positive Rate.

### 🔹 **R² Score**

Explains how much variance in the target variable is explained by the model.

### 🔹 **RMSE (Root Mean Squared Error)**

Measures the standard deviation of prediction errors:
$$ RMSE = \sqrt{\frac{1}{n}\sum(y_{true} - y_{pred})^2} $$

### 🔹 **MAE (Mean Absolute Error)**

Average of absolute errors:
$$ MAE = \frac{1}{n}\sum|y_{true} - y_{pred}| $$

### 🔹 **Silhouette Score**

Measures how well samples are clustered:

- Close to **1** → good clustering
- Close to **0** → overlapping clusters

### 🔹 **Inertia (Elbow Method)**

Sum of squared distances of samples to their nearest cluster center. Used to find optimal number of clusters.

---

## 📦 **Libraries Used**

### 🔹 **pandas** → Data handling and manipulation

### 🔹 **numpy** → Numerical operations

### 🔹 **matplotlib / seaborn** → Visualization

### 🔹 **scikit-learn (sklearn)** → ML algorithms, datasets, metrics, model selection utilities

---

## 🔑 **Important Functions Used**

| Function | Purpose |
|-----------|---------|
| `load_breast_cancer()` | Loads breast cancer dataset |
| `load_diabetes()` | Loads diabetes dataset |
| `load_iris()` | Loads iris dataset |
| `train_test_split()` | Splits dataset into train and test |
| `StratifiedKFold()` | Cross-validation for classification |
| `KFold()` | Cross-validation for regression |
| `cross_val_score()` | Computes CV score for a model |
| `fit()` | Trains the model |
| `predict()` | Makes predictions on data |
| `classification_report()` | Shows precision, recall, F1-score |
| `accuracy_score()` | Computes accuracy |
| `roc_auc_score()` | Computes ROC-AUC score |
| `mean_squared_error()` | Computes MSE for regression |
| `r2_score()` | Computes R² score |
| `PCA()` | Reduces data to fewer dimensions |
| `KMeans()` | Performs k-means clustering |
| `AgglomerativeClustering()` | Performs hierarchical clustering |
| `silhouette_score()` | Evaluates clustering quality |

---

## 🎯 **How to Use This Glossary?**

Use this file while running the scripts to **understand every method, metric, and ML concept** step by step.
