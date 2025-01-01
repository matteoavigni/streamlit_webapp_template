import streamlit as st
from auth.auth import login_button


login_button()
# if st.button("Log in"):
#     st.session_state.user = 'admin'
#     st.rerun()
