import streamlit as st
from auth.auth import logout


def is_logged_in():
    if st.session_state.get("user"):
        return True
    else:
        return False


def permission_denied():
    st.error("This page is not accessible for non authenticated users!")
    st.markdown("""
    <a href="app" target="_self">Go to the homepage</a>
    """, unsafe_allow_html=True)
