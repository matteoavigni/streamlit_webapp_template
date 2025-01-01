import streamlit as st
from utils import permission_denied


if "user" in st.session_state:
    st.title("Profile")
    st.image(st.session_state.user['picture'], width=150)
    st.write(f"Name: {st.session_state.user['name']}")
    st.write(f"Email: {st.session_state.user['email']}")
else:
    permission_denied()
