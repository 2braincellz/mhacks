#import streamlit as st
import streamlit as st
st.set_page_config(page_title="journal")


if st.button("Start Scanning"):
    st.write("Scanning initiated...")

uploaded_file = st.file_uploader("Upload your notes", type=["jpg", "png", "pdf"])
if uploaded_file is not None:
    st.success("File successfully uploaded!")

