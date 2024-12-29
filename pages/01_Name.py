import streamlit as st
from utils import permission_denied
from utils import sidebar_menu


def display():
    st.title("Name")
    st.write(f"Welcome, {st.session_state.user['name']}!")


if "user" in st.session_state:
    display()
else:
    permission_denied()
sidebar_menu()
