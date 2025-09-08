import pandas as pd
import numpy as np
from datetime import datetime, timedelta

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