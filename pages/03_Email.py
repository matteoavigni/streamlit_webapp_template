import streamlit as st
from utils import permission_denied
from utils import sidebar_menu


def display():
    st.title("Email")
    st.write(f"Your email address is {st.session_state.user['email']}!")


if "user" in st.session_state:
    display()
else:
    permission_denied()
sidebar_menu()
