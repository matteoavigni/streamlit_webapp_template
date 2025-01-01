import streamlit as st
from utils import permission_denied


if "user" in st.session_state:
    st.title("Email")
    st.write(f"Your email address is {st.session_state.user['email']}!")
else:
    permission_denied()
