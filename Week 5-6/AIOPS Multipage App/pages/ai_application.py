# pages/ai_application.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest

st.set_page_config(
    page_title="AI Application in AIOps",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI in AIOps: Beyond Hardcoded Thresholds")

st.markdown("""
One of the most powerful aspects of AIOps is its ability to leverage Artificial Intelligence and Machine Learning. Unlike traditional monitoring systems that rely on static, hardcoded thresholds (e.g., "alert if CPU > 80%"), AI models can learn the normal behavior of your systems and automatically detect subtle, complex, or evolving anomalies.

**Why AI is crucial in AIOps:**
* **Adaptive Learning:** AI models continuously learn from new data, adapting to changing system behaviors and seasonality.
* **Contextual Awareness:** They can consider multiple metrics and their relationships, detecting anomalies that a single threshold might miss.
* **Reduced False Positives:** By understanding "normal," AI significantly reduces the number of irrelevant alerts, combating alert fatigue.
* **Proactive Detection:** Identify nascent issues before they escalate into major incidents, often predicting problems before they are visible to the human eye.

In this demo, we'll use a Machine Learning algorithm (`IsolationForest` from `scikit-learn`) to detect anomalies in simulated system data, demonstrating its power over simple thresholding.
""")

st.subheader("Demo: Anomaly Detection with Machine Learning")

# --- Data Generation ---
def generate_complex_metric_data(num_points=200, anomaly_type='spike'):
    np.random.seed(42) # for reproducibility
    time_series = pd.date_range(start='2025-07-01 00:00:00', periods=num_points, freq='10min')

    # Simulate normal fluctuating behavior (e.g., daily cycles, general noise)
    # Base load with some daily pattern
    base_load = 50 + 15 * np.sin(np.linspace(0, 4 * np.pi, num_points))
    noise = np.random.normal(0, 5, num_points)
    metric_data = base_load + noise
    metric_data = np.clip(metric_data, 10, 90) # Keep within reasonable bounds

    # Introduce anomalies
    anomalies_indices = []
    if anomaly_type == 'spike':
        # Single large spike
        spike_idx = np.random.randint(num_points * 0.3, num_points * 0.7)
        metric_data[spike_idx] += np.random.uniform(40, 60)
        anomalies_indices.append(spike_idx)
    elif anomaly_type == 'drift':
        # Gradual drift over a period
        drift_start = np.random.randint(num_points * 0.4, num_points * 0.6)
        drift_end = min(drift_start + 20, num_points)
        metric_data[drift_start:drift_end] += np.linspace(0, 30, drift_end - drift_start)
        anomalies_indices.extend(range(drift_start, drift_end))
    elif anomaly_type == 'outlier_cluster':
        # A small cluster of outliers
        cluster_start = np.random.randint(num_points * 0.3, num_points * 0.7)
        for i in range(3):
            idx = cluster_start + i * 5
            if idx < num_points:
                metric_data[idx] += np.random.uniform(25, 45)
                anomalies_indices.append(idx)

    df = pd.DataFrame({
        "Timestamp": time_series,
        "Value": metric_data
    })
    return df, anomalies_indices

# --- Anomaly Detection with IsolationForest ---
def detect_anomalies_ml(df, column):
    # Train IsolationForest model
    # contamination: The proportion of outliers in the dataset.
    # A small value (e.g., 0.01-0.05) is often a good starting point for general anomaly detection.
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(df[[column]])

    # Predict anomalies (-1 for outliers, 1 for inliers)
    df['Anomaly_Score'] = model.decision_function(df[[column]])
    df['Anomaly'] = model.predict(df[[column]]) == -1
    return df

# User controls for simulation
num_points = st.slider("Number of data points:", 100, 500, 200, 50)
anomaly_choice = st.selectbox(
    "Choose anomaly type:",
    ('spike', 'drift', 'outlier_cluster')
)

if st.button("Run ML Anomaly Detection"):
    df_data, true_anomalies_indices = generate_complex_metric_data(num_points, anomaly_choice)
    df_results = detect_anomalies_ml(df_data, 'Value')

    st.subheader("Results:")

    fig, ax = plt.subplots(figsize=(14, 7))
    sns.lineplot(x='Timestamp', y='Value', data=df_results, ax=ax, label='Metric Value', color='blue')

    # Highlight detected anomalies
    detected_anomalies = df_results[df_results['Anomaly']]
    if not detected_anomalies.empty:
        sns.scatterplot(x='Timestamp', y='Value', data=detected_anomalies, color='red', s=150, label='ML Detected Anomaly', ax=ax, zorder=5)
        st.error(f"🚨 **ML Anomaly Detected!** The Isolation Forest model identified {len(detected_anomalies)} potential anomalies.")
    else:
        st.success("✅ No significant anomalies detected by the ML model.")

    ax.set_title("Metric Value Over Time with ML Anomaly Detection")
    ax.set_xlabel("Time")
    ax.set_ylabel("Metric Value")
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("""
    **Understanding the Demo:**
    * The blue line represents the simulated metric data, which includes a hidden anomaly (spike, drift, or cluster of outliers).
    * The red points indicate where the `IsolationForest` model automatically detected an anomaly. Notice how it identifies unusual patterns without you having to define a specific "high" or "low" threshold.
    * This is a simple example, but in our course, you'll learn to apply more sophisticated ML models and techniques to real-world AIOps data, enabling truly intelligent and proactive IT operations.
    """)

st.markdown("---")
st.markdown("© 2025 AIOps Demo. All rights reserved.")
