import streamlit as st
from utils import permission_denied


if "user" in st.session_state:
    st.title("Name")
    st.write(f"Welcome, {st.session_state.user['name']}!")
else:
    permission_denied()
