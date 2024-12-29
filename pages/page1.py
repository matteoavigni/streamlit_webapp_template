# pages/page1.py
import streamlit as st


def display():
    st.title("Name")
    st.write(f"Welcome, {st.session_state.user['name']}!")
