import streamlit as st
from utils import is_logged_in

st.markdown("""
# Homepage

## Welcome to the app template

This is a template app. Feel free to explore!

""")

if is_logged_in():
    st.page_link("pages/reserved_area.py", label="Reserved Area", icon=":material/dashboard:")

