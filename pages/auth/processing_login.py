import streamlit as st
from auth.auth import handle_oauth_callback

with st.spinner('Processing Login, please wait...'):
    handle_oauth_callback()
