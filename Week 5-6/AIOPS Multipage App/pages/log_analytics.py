# pages/log_analytics.py
import streamlit as st
import pandas as pd
import re

st.set_page_config(
    page_title="Log Analytics Demo",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Log Analytics: Understanding Your System's Story")

st.markdown("""
Log analytics is a foundational pillar of AIOps. Systems generate vast amounts of log data every second, which contains critical information about their health, performance, and potential issues. Manually sifting through these logs is impossible.

**What you'll learn in this section of the course:**
* **Log Parsing:** Extracting meaningful information from unstructured log lines.
* **Log Classification:** Categorizing logs (e.g., INFO, WARNING, ERROR) to prioritize and identify critical events.
* **Pattern Recognition:** Identifying recurring patterns that might indicate normal behavior or emerging problems.

In this demo, you can input sample log lines, and we'll show you how AIOps principles can automatically parse and classify them.
""")

st.subheader("Try It Yourself: Log Parser & Classifier")

# Sample log data for demonstration
sample_logs = """
2025-07-01 10:00:01 INFO User 'john.doe' logged in successfully from IP 192.168.1.10.
2025-07-01 10:00:05 WARNING Disk usage on /dev/sda1 is 85%. Approaching critical threshold.
2025-07-01 10:00:10 DEBUG Processing request for /api/data with ID 12345.
2025-07-01 10:00:15 ERROR Database connection failed: Connection refused at 10.0.0.5:5432.
2025-07-01 10:00:20 INFO Background task 'data_sync' completed in 120ms.
2025-07-01 10:00:22 WARNING High CPU utilization detected: 92% for process 'analytics_service'.
2025-07-01 10:00:25 ERROR File not found: /var/log/app/config.json.
"""

user_input_logs = st.text_area(
    "Enter your log lines here (or use the sample below):",
    value=sample_logs,
    height=250
)

# Function to parse and classify logs
def analyze_logs(log_data):
    # Regex to extract timestamp, log level, and message
    log_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (INFO|WARN|WARNING|ERROR|DEBUG|CRITICAL) (.*)")

    results = []
    for line in log_data.strip().split('\n'):
        match = log_pattern.match(line)
        if match:
            timestamp, level, message = match.groups()
            results.append({
                "Timestamp": timestamp,
                "Level": level,
                "Message": message,
                "Original Log": line
            })
        else:
            results.append({
                "Timestamp": "N/A",
                "Level": "UNKNOWN",
                "Message": "Could not parse log line.",
                "Original Log": line
            })
    return pd.DataFrame(results)

if st.button("Analyze Logs"):
    if user_input_logs:
        df_logs = analyze_logs(user_input_logs)
        st.subheader("Analysis Results:")
        st.dataframe(df_logs, use_container_width=True)

        st.markdown("---")
        st.subheader("Key Insights from Log Analysis:")
        # Simple aggregation for insights
        level_counts = df_logs['Level'].value_counts()
        st.write("Distribution of Log Levels:")
        st.bar_chart(level_counts)

        if 'ERROR' in level_counts and level_counts['ERROR'] > 0:
            st.error(f"🚨 **Attention:** Detected {level_counts['ERROR']} ERROR logs. These require immediate investigation!")
            st.write("Example Error Logs:")
            st.dataframe(df_logs[df_logs['Level'] == 'ERROR'])
        if 'WARNING' in level_counts and level_counts['WARNING'] > 0:
            st.warning(f"⚠️ **Warning:** Detected {level_counts['WARNING']} WARNING logs. These indicate potential issues.")
            st.write("Example Warning Logs:")
            st.dataframe(df_logs[df_logs['Level'] == 'WARNING'])
        if 'INFO' in level_counts and level_counts['INFO'] > 0:
            st.info(f"ℹ️ **Info:** Detected {level_counts['INFO']} INFO logs. These provide general operational information.")

        st.markdown("""
        This simple demo highlights how AIOps automates the tedious task of log analysis, allowing IT teams to quickly
        identify critical events and focus their efforts where they're most needed, rather than manually scanning thousands of lines.
        In our course, you'll learn advanced techniques for log parsing, sentiment analysis, and correlation.
        """)
    else:
        st.warning("Please enter some log lines to analyze.")

st.markdown("---")
st.markdown("© 2025 AIOps Demo. All rights reserved.")
