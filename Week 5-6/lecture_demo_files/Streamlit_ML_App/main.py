import streamlit as st
import plotly.graph_objects as go
from utils import *

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


col1, col2 = st.columns([0.7, 0.3])

with col2:
    st.subheader("User inputs")
    num_points = st.slider("Number of Data Points", min_value=50, max_value=500, value=200, step=50)
    if st.button("Generate New Data"):
        st.session_state.data = generate_synthetic_data()
        st.rerun()
    threshold = st.slider("Z-score Threshold", min_value=1.0, max_value=3.0, value=2.0, step=0.5)
    window_size = st.slider("Rolling Window Size", min_value=5, max_value=30, value=10, step=1)


with col1:
    st.subheader("Simulated CPU Usage Over Time")

    # State management for data regeneration
    if 'data' not in st.session_state:
        st.session_state.data = generate_synthetic_data(num_points=200)

    # Plotting with Plotly
    fig = go.Figure()

    data = st.session_state.data
    
    df_processed = detect_anomalies_zscore(st.session_state.data, 'cpu_usage', threshold)
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
