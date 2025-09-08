import streamlit as st
import pandas as pd
import time

uploaded_file = st.file_uploader("Upload a file")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

st.title("My First Streamlit App")
st.write("Hello, world!")

# st.header("Section Header")
# st.subheader("Subsection Header")

# with st.expander("Click to expand"):
#     if uploaded_file is not None:
#         st.dataframe(df)

# checked = st.checkbox("want to see chart?")
# st.write(checked)

@st.cache_data
def sleepy_func(t=3):
    st.write("Going to sleep...for ", t, " seconds")
    time.sleep(t)
    st.write("Woke up!")
    return t**2

tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
with tab1:
    st.write("Content for Tab 1")

    value = st.slider("Select a value", 1, 5, 3)
    st.write(f"You selected: {value}")
    if st.button("Sleep for x seconds"):
        output =sleepy_func(value)
        st.write(f"Output: {output}")

with tab2:
    st.write("Content for Tab 2")

# if checked:
#     option = st.radio("Choose an option", ("show", "hide"), index=1)
#     if option == "show":
#         st.write("You chose to show the chart.")
#         # if st.button("show chart", type="primary"):
#         st.write("Button clicked!")
#         st.line_chart(df)



# name = st.text_input("Enter your name")
# st.write(f"Hello, {name}!")


