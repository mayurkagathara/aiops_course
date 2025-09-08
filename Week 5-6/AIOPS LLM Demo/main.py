
import streamlit as st
from analyzer.parser import extract_log_sections
from analyzer.llm_interface import ask_llm_ollama

st.set_page_config(page_title="Log Inspector", page_icon="🤖", layout="wide")
st.title("🔍 Log File Inspector")

# Session state to store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader("Upload a log file", type=["log", "txt"])

if uploaded_file:
    # Track uploaded file name to reset session if changed
    if "last_uploaded_filename" not in st.session_state or \
       st.session_state.last_uploaded_filename != uploaded_file.name:

        # New file detected → reset everything
        st.session_state.last_uploaded_filename = uploaded_file.name
        st.session_state.chat_history = []
        st.session_state.pop("log_summary", None)
    
    content = uploaded_file.read().decode()
    st.subheader("📄 Log Preview")
    st.text_area("Raw Log Contents", value=content[:2000], height=200)

    # Extract log sections once
    log_chunks = extract_log_sections(content)
    print(log_chunks)

    # 🔹 Auto-summary panel
    if "log_summary" not in st.session_state:
        with st.spinner("Summarizing log..."):
            summary_prompt = f"Summarize the following log file:\n\n{chr(10).join(log_chunks[:5])}"
            summary = ask_llm_ollama(summary_prompt)
            st.session_state.log_summary = summary

    st.markdown("### 📊 Log Summary")
    st.write(st.session_state.log_summary)

    # 🔹 Chat UI
    st.markdown("### 💬 Ask Questions")
    user_query = st.text_input("Type your question about the log", key="user_question")

    if user_query:
        with st.spinner("Analyzing..."):
            prompt = f"""You are analyzing a system log.

--- LOG SNIPPET START ---
{chr(10).join(log_chunks[:5])}
--- LOG SNIPPET END ---

Question: {user_query}
Provide a clear and concise answer."""
            response = ask_llm_ollama(prompt)
            st.session_state.chat_history.append((user_query, response))

    # Display chat history
    for user_question, ai_response in st.session_state.chat_history:
        st.markdown(f"**🧑‍💻 You:** {user_question}")
        st.markdown(f"**🤖 AI:** {ai_response}")
        st.markdown("---")
