# 📘 Glossary and ML Workflow Cheatsheet

This file explains **all jargon and technical terms**, plus a **step-by-step ML workflow**, **common issues**, and **tips to solve them**.

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

---

## 🔄 **Overall Machine Learning Cycle**

1️⃣ **Understand the Problem**  
   – Is it **classification, regression, or clustering**?  
   – Identify input (features) and output (target).

2️⃣ **Data Collection / Loading**  
   – Load built-in datasets (e.g., `load_breast_cancer()`, `load_diabetes()`).

3️⃣ **Exploratory Data Analysis (EDA)**  
   – Check shape, missing values, distributions, correlations.  
   – Visualize data to spot patterns or class imbalance.

4️⃣ **Data Preprocessing**  
   – Handle missing values, scaling, encoding (if needed).  
   – Feature selection/dimensionality reduction (PCA).

5️⃣ **Split Data**  
   – Use `train_test_split()` (Stratified for classification).

6️⃣ **Model Selection**  
   – Start with simple models (Logistic/Linear Regression).  
   – Try advanced models (RandomForest, Ridge, etc.).

7️⃣ **Validation**  
   – Use `cross_val_score()` with **KFold/StratifiedKFold**.  
   – Compare metrics (Accuracy, R², RMSE, etc.).

8️⃣ **Prediction & Evaluation**  
   – Check test performance.  
   – Use confusion matrix, ROC-AUC (for classification).

9️⃣ **Model Improvement**  
   – Hyperparameter tuning.  
   – Try different algorithms, more data, feature engineering.

10️⃣ **Deployment or Reporting**  
   – Save model, share predictions, or integrate into apps.

---

## ⚠️ **Common Problems and Solutions**

### 📌 **1. Poor Validation Accuracy**

✅ Causes:

- Overfitting to training data.
- Class imbalance.
- Irrelevant or redundant features.

✅ Solutions:

- Use **cross-validation (KFold)** to get stable scores.
- Perform **feature selection** (drop highly correlated features).
- Collect more data or add regularization (e.g., Ridge, Lasso).

---

### 📌 **2. Class Imbalance in Classification**

✅ Causes:

- One class dominates dataset (e.g., 90% negative, 10% positive).

✅ Solutions:

- Use **Stratified Train-Test Split**.
- Evaluate with **Precision, Recall, F1-score**, not just accuracy.
- Use oversampling (SMOTE) or class weights in models.

---

### 📌 **3. Overfitting (High Train Accuracy, Low Test Accuracy)**

✅ Causes:

- Model too complex (e.g., deep tree).
- Too many features vs. samples.

✅ Solutions:

- Use simpler models or regularization (Ridge/Lasso).
- Try **cross-validation**.
- Get more training data.

---

### 📌 **4. Underfitting (Low Accuracy in Both Train and Test)**

✅ Causes:

- Model too simple (e.g., Linear Regression for complex data).

✅ Solutions:

- Try more powerful models (RandomForest, Gradient Boosting).
- Add interaction features or polynomial terms.

---

### 📌 **5. Clustering Issues (Wrong Number of Clusters)**

✅ Causes:

- Choosing wrong `k` in KMeans.

✅ Solutions:

- Use **Elbow Method (Inertia)** to find optimal k.
- Check **Silhouette Score** for cluster quality.

---

## 🎯 **Key Tips for Beginners**

🔹 Always **start with EDA** – understand your data before training.  
🔹 **Use CV (KFold/StratifiedKFold)** to avoid misleading single-split results.  
🔹 Compare **multiple metrics** (Accuracy, F1, ROC-AUC for classification; R², RMSE for regression).  
🔹 For clustering, always **visualize clusters (PCA, scatter plots)**.  
🔹 Don’t rely on just one model – **try different algorithms**.

---

The first part of this file still contains **Glossary definitions** for all terms used in code. The second part is this **ML Workflow Cheatsheet** to guide you step by step.
