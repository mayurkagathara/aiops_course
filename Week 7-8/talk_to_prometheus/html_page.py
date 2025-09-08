import streamlit as st
import streamlit.components.v1 as components
import os
import webbrowser

# Path to your local HTML file
html_file_path = r"C:\Users\admin\Documents\VP\Week 7-8\talk_to_prometheus\crewai_flow.html" # Replace with the actual path

if os.path.exists(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Create a data URI for the HTML content
    # This embeds the HTML directly into the URL, allowing it to open in a new tab
    # without needing a web server to serve the local file.
    data_uri = "data:text/html;charset=utf-8," + html_content

    # JavaScript to open the data URI in a new tab
    js_code = f"""
    <script type="text/javascript">
        window.open('{data_uri}', '_blank').focus();
    </script>
    """
    #js_code_2 to open the local html file directly in new window file:///C:/Users/admin/Documents/VP/Week%207-8/talk_to_prometheus/crewai_flow.html
    js_code_2 = f"""
    <script type="text/javascript">
        window.open('file:///C:/Users/admin/Documents/VP/Week%207-8/talk_to_prometheus/crewai_flow.html', '_blank');
    </script>
    """

    st.button("Open Local HTML in New Tab", on_click=lambda: components.html(js_code, height=0, width=0))
    st.button("Open Local HTML in New Tab 2", on_click=lambda: components.html(js_code_2, height=0, width=0))

    html_file_name = "crewai_flow.html"
    html_file_path = os.path.abspath(html_file_name)
    if st.button("Open Flow HTML file in New Tab"):
        # Open the HTML file in a new browser window/tab
        webbrowser.open(f"file:///{html_file_path}", new=2)
        st.success("Local HTML file opened in a new window/tab.")



else:
    st.error(f"HTML file not found at: {html_file_path}")