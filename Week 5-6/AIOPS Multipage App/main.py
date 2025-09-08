# main_app.py
import streamlit as st

st.set_page_config(
    page_title="AIOps Demo Lecture",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Main Page Content ---
st.title("🤖 Welcome to the AIOps Demo Lecture!")

st.markdown("""
Welcome, working professionals! In today's session, we'll explore the transformative power of AIOps (Artificial Intelligence for IT Operations) and how it's revolutionizing the way IT operations are managed. This demo will give you a glimpse into what you'll achieve by taking our comprehensive AIOps course.

**Why AIOps?**
In today's complex IT environments, traditional monitoring and manual troubleshooting simply can't keep up. We're drowning in data, facing alert fatigue, and struggling with slow incident resolution. AIOps leverages Artificial Intelligence and Machine Learning to bring intelligence, automation, and proactive capabilities to IT operations.

**What You'll Discover in This Demo:**
Through this interactive demonstration, you'll see how AIOps can help you:
* **Automate Log Analysis:** Quickly parse, classify, and understand vast amounts of log data.
* **Detect Anomalies in Metrics:** Proactively identify unusual patterns in system metrics before they cause outages.

These are just a few examples of the powerful skills you'll gain in our course, designed to enhance your current job role and propel your career forward in the rapidly growing field of AIOps.

Use the sidebar on the left to navigate through the different AIOps demo pillars!
""")

st.subheader("What is AIOps?")
st.markdown("""
AIOps stands for **Artificial Intelligence for IT Operations**. It's a multi-layered technology platform that automates and enhances IT operations by combining:
* **Big Data:** Ingesting and processing massive volumes of operational data (logs, metrics, events, traces).
* **Machine Learning:** Applying advanced algorithms to analyze this data, identify patterns, detect anomalies, predict issues, and automate responses.

**Goals of AIOps:**
* **Reduce Alert Noise:** Filter out irrelevant alerts and prioritize critical issues.
* **Faster Root Cause Analysis:** Quickly pinpoint the source of problems.
* **Proactive Issue Detection:** Identify and resolve potential problems before they impact users.
* **Automate Repetitive Tasks:** Free up IT staff from manual, tedious work.
* **Improve Operational Efficiency:** Streamline workflows and reduce Mean Time To Resolution (MTTR).
""")

st.subheader("Why is AIOps Crucial for Working Professionals?")
st.markdown("""
* **Career Advancement:** AIOps skills are in high demand, opening doors to specialized roles like AIOps Engineer, Site Reliability Engineer (SRE), and DevOps roles.
* **Enhanced Job Performance:** Directly apply AIOps techniques to your current role to reduce manual effort, improve system reliability, and become a more proactive problem-solver.
* **Future-Proof Your Skills:** As IT environments become more complex and data-driven, AIOps expertise will be essential for navigating the future of operations.
* **Increased Earning Potential:** Specialized skills in a growing field often lead to higher compensation.
""")

st.info("Ready to see AIOps in action? Select a demo from the sidebar!")

# Add a simple footer
st.markdown("---")
st.markdown("© 2025 AIOps Demo. All rights reserved.")
