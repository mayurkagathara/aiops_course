# aio_demo_app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(layout="wide", page_icon="📊", page_title="AIOps Anomaly Detection Demo")

st.title("📊 AIOps Live Demo: Anomaly Detection for System Metrics")
st.markdown("---")

st.write(
    """
    This interactive demo illustrates a core AIOps concept: **Anomaly Detection**.
    We'll simulate system CPU utilization data and use a simple statistical method (Z-score)
    to identify unusual spikes or drops, just like how AIOps helps spot issues proactively.
    (This concept is covered in **Week 3, Day 14** of the Visualpath AIOps course!) 
    """
)

# --- Data Generation Function ---
def generate_synthetic_data(num_points=200):
    # np.random.seed(42) # for reproducibility
    base_cpu = np.random.normal(loc=40, scale=5, size=num_points)
    
    # Introduce some "normal" fluctuations
    cpu_data = base_cpu + np.sin(np.linspace(0, 10, num_points)) * 5

    # Introduce anomalies (spikes)
    anomaly_indices = np.random.choice(num_points, 5, replace=False)
    for idx in anomaly_indices:
        cpu_data[idx] += np.random.uniform(20, 40) # Add significant spike

    # Ensure no negative values
    cpu_data = np.maximum(cpu_data, 0)
    
    timestamps = [datetime.now() - timedelta(minutes=(num_points - 1 - i) * 5) for i in range(num_points)]
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'cpu_usage': cpu_data
    })
    df.set_index('timestamp', inplace=True)
    return df

# --- Anomaly Detection Function (Z-score based) ---
def detect_anomalies_zscore(df, column, threshold=2.0, window=10):
    """
    Detects anomalies using a rolling Z-score method.
    """
    df_copy = df.copy()
    
    # Calculate rolling mean and standard deviation
    df_copy['rolling_mean'] = df_copy[column].rolling(window=window, min_periods=1).mean()
    df_copy['rolling_std'] = df_copy[column].rolling(window=window, min_periods=1).std()
    
    # Calculate Z-score
    df_copy['z_score'] = (df_copy[column] - df_copy['rolling_mean']) / df_copy['rolling_std']
    
    # Mark anomalies
    # Handle NaN z_score (e.g., at beginning where std is 0 or NaN)
    df_copy['is_anomaly'] = (np.abs(df_copy['z_score']) > threshold) & (df_copy['rolling_std'].notna()) & (df_copy['rolling_std'] != 0)
    
    return df_copy

# --- Streamlit UI ---

col1, col2 = st.columns([0.7, 0.3])

with col1:
    st.subheader("Simulated CPU Usage Over Time")
    
    # State management for data regeneration
    if 'data' not in st.session_state:
        st.session_state.data = generate_synthetic_data()

    # User input for Z-score threshold
    z_score_threshold = st.slider(
        "Adjust Anomaly Detection Sensitivity (Z-score Threshold)",
        min_value=1.0, max_value=4.0, value=2.5, step=0.1,
        help="Lower threshold = more sensitive (more anomalies detected), Higher threshold = less sensitive."
    )

    # Perform anomaly detection
    df_processed = detect_anomalies_zscore(st.session_state.data, 'cpu_usage', threshold=z_score_threshold)
    
    # Plotting with Plotly
    fig = go.Figure()

    # Original data trace
    fig.add_trace(go.Scatter(x=df_processed.index, y=df_processed['cpu_usage'],
                             mode='lines', name='CPU Usage (%)', line=dict(color='blue')))

    # Anomalies trace
    anomalies = df_processed[df_processed['is_anomaly']]
    if not anomalies.empty:
        fig.add_trace(go.Scatter(x=anomalies.index, y=anomalies['cpu_usage'],
                                 mode='markers', name='Detected Anomaly',
                                 marker=dict(color='red', size=10, symbol='circle',
                                             line=dict(width=1, color='DarkSlateGrey'))))

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="CPU Usage (%)",
        hovermode="x unified",
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Demo Controls & Insights")

    st.write("Click 'Generate New Data' to see different patterns and anomalies.")
    if st.button("Generate New Data"):
        st.session_state.data = generate_synthetic_data()
        st.rerun()
    
    st.markdown("---")
    
    st.write("**How Anomaly Detection Works Here:**")
    st.markdown(
        """
        1.  **Data Ingestion:** We simulate continuous CPU metric data. [cite: 19]
        2.  **Statistical Analysis:** We calculate a rolling Z-score for each data point. The Z-score measures how many standard deviations a data point is from the rolling mean. 
        3.  **Thresholding:** If a data point's Z-score exceeds the set 'Sensitivity Threshold', it's flagged as an anomaly. [cite: 33]
        4.  **Visualization:** Anomalies are highlighted in real-time on the graph, providing immediate visual alerts. [cite: 41]
        """
    )
    
    st.markdown("---")
    st.info(
        f"**Detected Anomalies:** {df_processed['is_anomaly'].sum()} out of {len(df_processed)} data points flagged."
    )

st.markdown("---")
st.caption("This demo is simplified for illustration. Real-world AIOps uses more sophisticated ML models and integrates with various data sources.")