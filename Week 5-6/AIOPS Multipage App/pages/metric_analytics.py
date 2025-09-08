# pages/metric_analytics.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Metric Analytics Demo",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Metric Analytics: Predicting the Future of Your Systems")

st.markdown("""
Metrics are numerical data points collected over time, such as CPU utilization, memory usage, network latency, or disk I/O. Analyzing these metrics is crucial for understanding system health and performance. However, manually monitoring thousands of metrics across a complex infrastructure is impossible.

**What you'll learn in this section of the course:**
* **Metric Collection:** How to gather system metrics using tools like `psutil`.
* **Time-Series Analysis:** Understanding trends and patterns in metric data.
* **Anomaly Detection:** Automatically identifying unusual deviations that could indicate an impending problem or an ongoing issue.
* **Predictive Analytics:** Forecasting future metric behavior to prevent outages.

In this demo, we'll simulate a common metric (e.g., CPU utilization) and apply a simple anomaly detection technique to highlight unusual behavior.
""")

st.subheader("Try It Yourself: Metric Anomaly Detection")

# Generate synthetic data with an anomaly
def generate_metric_data(num_points=100, anomaly_start=70, anomaly_duration=5, anomaly_magnitude=0.3):
    time_series = pd.date_range(start='2025-07-01 09:00:00', periods=num_points, freq='5min')
    # Simulate normal CPU usage (e.g., around 40-60%)
    cpu_usage = np.random.normal(loc=50, scale=5, size=num_points)
    cpu_usage = np.clip(cpu_usage, 0, 100) # Keep within 0-100%

    # Introduce an anomaly (e.g., a sudden spike)
    if anomaly_start < num_points:
        end_anomaly = min(anomaly_start + anomaly_duration, num_points)
        cpu_usage[anomaly_start:end_anomaly] += anomaly_magnitude * np.random.uniform(20, 40, size=(end_anomaly - anomaly_start))
        cpu_usage = np.clip(cpu_usage, 0, 100)

    df = pd.DataFrame({
        "Timestamp": time_series,
        "CPU_Usage": cpu_usage
    })
    return df, anomaly_start, end_anomaly

# Simple Z-score based anomaly detection
def detect_anomalies_zscore(df, column, threshold=2.5):
    mean = df[column].mean()
    std = df[column].std()
    df['Z_Score'] = (df[column] - mean) / std
    df['Anomaly'] = np.abs(df['Z_Score']) > threshold
    return df

num_data_points = st.slider("Number of data points to simulate:", 50, 200, 100)
anomaly_position = st.slider("Position of anomaly (approx. % of data):", 10, 90, 70)
anomaly_strength = st.slider("Anomaly strength (magnitude):", 0.1, 1.0, 0.5)

df_metrics, anomaly_start_idx, anomaly_end_idx = generate_metric_data(
    num_points=num_data_points,
    anomaly_start=int(num_data_points * (anomaly_position / 100)),
    anomaly_duration=int(num_data_points * 0.05), # 5% of data points
    anomaly_magnitude=anomaly_strength
)

df_metrics_anomalies = detect_anomalies_zscore(df_metrics, 'CPU_Usage')

if st.button("Generate & Analyze Metrics"):
    st.subheader("Simulated CPU Usage with Anomaly Detection:")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='Timestamp', y='CPU_Usage', data=df_metrics_anomalies, ax=ax, label='CPU Usage')

    # Highlight anomalies
    anomalies = df_metrics_anomalies[df_metrics_anomalies['Anomaly']]
    if not anomalies.empty:
        sns.scatterplot(x='Timestamp', y='CPU_Usage', data=anomalies, color='red', s=100, label='Anomaly Detected', ax=ax, zorder=5)
        st.error(f"🚨 **Anomaly Detected!** Unusual CPU usage detected at multiple points. This could indicate a performance issue or an attack.")
    else:
        st.success("✅ No significant anomalies detected in the current simulation.")

    ax.set_title("CPU Usage Over Time with Anomaly Detection")
    ax.set_xlabel("Time")
    ax.set_ylabel("CPU Usage (%)")
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("""
    This visualization demonstrates how AIOps can automatically identify deviations from normal behavior.
    Instead of manually setting thresholds or constantly watching dashboards, AIOps uses machine learning
    to learn baselines and flag anomalies, allowing you to be proactive.
    In our course, you'll delve deeper into various anomaly detection algorithms and their practical applications.
    """)

st.markdown("---")
st.markdown("© 2025 AIOps Demo. All rights reserved.")
