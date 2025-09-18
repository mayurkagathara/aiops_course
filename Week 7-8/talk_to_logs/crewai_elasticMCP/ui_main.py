import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from ui_utils_backend import get_distinct_values, search_documents

st.set_page_config(page_title="Elasticsearch", layout="wide", page_icon="🤖")

INDEX_NAME = "logs-aiops_demo_semantic"
FIELD_LIST = [
    "customer",
    "log_level",
    "log_type",
    "environment_name",
    "application_name",
]
PAGE_SIZE = 100

# --- Initialize Session State ---

session_state_variables = [
    ("unique_data", None),
    ("search_results", []),
    ("total_hits", 0),
    ("page", 1),
    ("filters", {}),
    ("user_query", ""),
    ("enable_knn", False),
    ("knn_results", 10),
    ("model", None),
]

for session_state_variable in session_state_variables:
    if session_state_variable[0] not in st.session_state:
        st.session_state[session_state_variable[0]] = session_state_variable[1]

# --- Streamlit UI Code ---

st.title("Elasticsearch Search🔎")
st.write("Use the dropdowns to filter the data and click 'Submit' to search.")

main_page_cols = st.columns([70, 30], vertical_alignment="top")

with main_page_cols[0]:
    if not st.session_state.model:
        with st.spinner("🔄Loading the embedding model"):
            st.session_state.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    # Load the distinct values
    if st.button("Load/Refresh data"):
        with st.spinner("📋Loading data..."):
            st.session_state.unique_data = get_distinct_values(INDEX_NAME, FIELD_LIST)


    # Use st.form to group widgets and add a submit button
    if st.session_state.unique_data:
        with st.form("search_form", border=True):
            selected_filters = {}
            first_row_cols = st.columns(
                len(FIELD_LIST), vertical_alignment="bottom", gap="medium"
            )
            for col, field in zip(first_row_cols, FIELD_LIST):
                with col:
                    options = ["All"] + st.session_state.unique_data.get(field, [])
                    selected_filters[field] = st.selectbox(
                        label=f"{field.replace('_', ' ').title()}",
                        options=options,
                        key=f"selectbox_{field}",
                    ).split("  (")[0]

            second_row_cols = st.columns(3, vertical_alignment="bottom", gap="medium")
            with second_row_cols[0]:
                start_date_cols = st.columns(2, vertical_alignment="bottom", gap="medium")
                with start_date_cols[0]:
                    start_date = st.date_input(
                        "Start Date",
                        value=None,
                        min_value=None,
                        max_value=None,
                        key="start_date",
                    )
                with start_date_cols[1]:
                    start_time = st.time_input(
                        "Start Time", value="00:00", key="start_time"
                    )
                if start_date and start_time:
                    start_datetime = pd.Timestamp.combine(start_date, start_time)
                    selected_filters["start_date"] = start_datetime.strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    )
                else:
                    selected_filters["start_date"] = None

            with second_row_cols[1]:
                end_date_cols = st.columns(2, vertical_alignment="bottom", gap="medium")
                with end_date_cols[0]:
                    end_date = st.date_input(
                        "End Date",
                        value=None,
                        min_value=None,
                        max_value=None,
                        key="end_date",
                    )
                with end_date_cols[1]:
                    end_time = st.time_input("End Time", value="00:00", key="end_time")
                if end_date and end_time:
                    end_datetime = pd.Timestamp.combine(end_date, end_time)
                    selected_filters["end_date"] = end_datetime.strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    )
                else:
                    selected_filters["end_date"] = None

            # print(selected_filters)

            user_query = st.text_input("Ask to elasticsearch: ")

            knn_cols = st.columns([1,5], vertical_alignment="bottom", gap="medium")

            with knn_cols[0]:
                enable_knn = st.checkbox("Enable KNN", value=True)
            with knn_cols[1]:
                knn_results = st.slider("KNN results", 1, 50, 10)

            with second_row_cols[2]:
                if st.form_submit_button("Search", type="secondary", icon="🕵️"):
                    # Reset to the first page and save the new filters on submit
                    st.session_state.user_query = user_query
                    st.session_state.page = 1
                    st.session_state.filters = selected_filters
                    st.session_state.enable_knn = enable_knn
                    st.session_state.knn_results = knn_results
                    with st.spinner("Searching..."):
                        st.session_state.search_results, st.session_state.total_hits = (
                            search_documents(
                                INDEX_NAME,
                                st.session_state.filters,
                                st.session_state.page,
                                PAGE_SIZE,
                                st.session_state.enable_knn,
                                st.session_state.knn_results,
                                st.session_state.user_query,
                            )
                        )

    # Display search results if available
    if st.session_state.search_results:
        st.subheader(f"Search Results ({st.session_state.total_hits})")
        # Convert results to a pandas DataFrame for a nice display
        results_df = pd.DataFrame(st.session_state.search_results)
        st.dataframe(
            results_df,
            hide_index=True,
        )

        # --- Pagination controls ---
        total_pages = (st.session_state.total_hits + PAGE_SIZE - 1) // PAGE_SIZE

        # Create columns for pagination buttons
        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            if st.session_state.page > 1:
                if st.button("Previous"):
                    st.session_state.page -= 1
                    st.session_state.search_results, st.session_state.total_hits = (
                        search_documents(
                            INDEX_NAME,
                            st.session_state.filters,
                            st.session_state.page,
                            PAGE_SIZE,
                            st.session_state.enable_knn,
                            st.session_state.knn_results,
                            st.session_state.user_query,
                        )
                    )
                    st.rerun()  # Rerun to update the results

        with col2:
            st.write(f"Page {st.session_state.page} of {total_pages}")

        with col3:
            if st.session_state.page < total_pages:
                if st.button("Next"):
                    st.session_state.page += 1
                    st.session_state.search_results, st.session_state.total_hits = (
                        search_documents(
                            INDEX_NAME,
                            st.session_state.filters,
                            st.session_state.page,
                            PAGE_SIZE,
                            st.session_state.enable_knn,
                            st.session_state.knn_results,
                            st.session_state.user_query,
                        )
                    )
                    st.rerun()  # Rerun to update the results

    else:
        st.warning(
            "❌ No results found. Load/refresh the data, fill the form and click on submit."
        )

with main_page_cols[1]:
    with st.spinner("🔄Loading CrewAI..."):
        import pandas as pd
        from ui_agentic_backend import LogAnalysisCrew

        # --- Initialize CrewAI and chat session state ---
        if "crew_manager" not in st.session_state:
            st.session_state.crew_manager = LogAnalysisCrew()

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []  # [(role, message), ...]

    st.subheader("💬 Talk to CrewAI")

    # --- Chat display ---
    chat_container = st.container()
    with chat_container:
        for role, msg in st.session_state.chat_history:
            if role == "user":
                st.markdown(f"**You:** {msg}")
            else:
                st.markdown(f"**CrewAI:**\n\n{msg}")

    # --- Auto-scroll to bottom ---
    scroll_js = """
    <script>
    var chatContainer = window.parent.document.querySelector('.main');
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    </script>
    """
    st.components.v1.html(scroll_js, height=0)

    # --- User input ---
    user_query = st.text_input("Ask CrewAI about results", key="chat_input")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Send"):
            if user_query.strip():
                # Save user query
                st.session_state.chat_history.append(("user", user_query))

                # Prepare context for CrewAI
                filters = st.session_state.filters or {}
                results = st.session_state.search_results or []

                # Keep only max 100 results and drop message_vector
                trimmed_results = []
                for r in results[:100]:
                    if isinstance(r, dict):
                        r.pop("message_vector", None)
                    trimmed_results.append(r)

                # Pass to CrewAI
                with st.spinner("🤖 Thinking..."):
                    answer = st.session_state.crew_manager.analyze(
                        filters, trimmed_results, user_query
                    )

                # Save CrewAI response
                st.session_state.chat_history.append(("crewai", answer))
                st.rerun()

    with col2:
        if st.button("Start New Chat"):
            st.session_state.crew_manager.reset_memory()
            st.session_state.chat_history = []
            st.success("✅ New chat started. Memory cleared.")
            st.rerun()
