import streamlit as st


def display():
    st.title("Email")
    st.write(f"Your email address is {st.session_state.user['email']}!")
