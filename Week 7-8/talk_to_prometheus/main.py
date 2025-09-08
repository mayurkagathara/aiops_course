print("importing modules...")
import os
import webbrowser
import json
from datetime import datetime
import streamlit as st
from flow_define import PromQLFlow
import plotly.express as px
print("modules imported successfully.")
# --- 7. Main Orchestrator ---

CLI_MODE = False

def cli_main():
    print("🚀 Starting the Prometheus PromQL Generation Flow...")
    try:
        # Create and run flow directly
        user_input = input("Ask to prometheus: ")
        user_query = f"{user_input}. current epoch is {int(datetime.now().timestamp())}"
        flow = PromQLFlow(original_query=user_query, retry_count=1)
        print("saving the flow as html file...")
        flow.plot()
        print("saved successfully!")

        final_state = flow.kickoff()
        try:
            print("\n--- Final Workflow State ---\n", final_state)
            print(json.dumps(final_state.model_dump_json(), indent=2))
        except Exception as e:
            print(str(e))
            raise

    except Exception as e:
        import traceback
        print(f"\n❌ Error during workflow execution: {str(e)} \n {traceback.format_exc()}")

def ui_main():
    """To define the streamlit interface. 
    First get input from user. spinner and then show the markdown output. 
    Also plot the graph for metrix."""

    #page mode wide
    st.set_page_config(layout="wide")

    st.title("Talk to Prometheus")
    st.write("This is a simple demo of CrewAI flow for converting user query to PromQL.")
    user_input = st.text_input("Ask to prometheus: ")
    user_query = f"{user_input}. current epoch is {int(datetime.now().timestamp())}"

    if not st.session_state.get("final_state"):
        st.session_state.final_state = None
    
    run_col, visualize_col = st.columns([0.1, 0.9])
    with run_col:
        if st.button("Ask AI"):
            st.session_state.flow = PromQLFlow(original_query=user_query, retry_count=1)
            with st.spinner("Running flow..."):
                st.session_state.final_state = st.session_state.flow.kickoff()

    with visualize_col:
        if st.button("visualize flow"):
            if not st.session_state.get("flow"):
                with st.spinner("creating the flow..."):
                    st.session_state.flow = PromQLFlow(original_query=user_query, retry_count=1)
            html_file_name = "promql_flow"
            st.session_state.flow.plot(filename=html_file_name)
            html_file_path = os.path.abspath(html_file_name+".html")
            webbrowser.open(f"file:///{html_file_path}", new=2)
            st.success("Local HTML flow file opened in a new window/tab.")

    if st.session_state.final_state:
        col1, col2 = st.columns(spec=[0.6, 0.4])
        with col1:
            try:
                st.markdown("### AI Analysis")
                st.markdown(st.session_state.final_state.final_answer)
                st.json(st.session_state.final_state.model_dump_json(), expanded=False)
            except Exception as e:
                st.write(str(e))
                raise

        with col2:
            st.session_state.chart_type = st.selectbox("Select chart type", ["line", "bar"], )
            if st.button("View Graph"):
                final_state_json = json.loads(st.session_state.final_state.model_dump_json())
                all_results = final_state_json.get("final_prometheus_result")['data']["result"]
                #plot metrics with line or bar chart (dowpdown option), using plotly
                x_timestamp = [datetime.fromtimestamp(x[0]) for x in all_results[0]['values']]
                y_metric_all = []
                print(x_timestamp,'\n', y_metric_all)
                for result in all_results:
                    metrics = result['metric']
                    values = result['values']
                    y_single_plot = [y[1] for y in values]
                    y_metric_all.append(y_single_plot)
                if st.session_state.chart_type == "line":
                    fig = px.line(x=x_timestamp, y=y_metric_all)
                elif st.session_state.chart_type == "bar":
                    fig = px.bar(x=x_timestamp, y=y_metric_all)
                    
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig)

if __name__ == "__main__":
    if CLI_MODE:
        cli_main()
    else:
        ui_main()
