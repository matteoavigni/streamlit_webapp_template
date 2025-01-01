import streamlit as st
from auth.auth import logout


logout()
# if st.button("Log out"):
#     st.session_state.user = None
#     st.rerun()
