import streamlit as st
from frontend import check_session

if not check_session():
    st.switch_page('frontend.py')

st.write("files.py")
