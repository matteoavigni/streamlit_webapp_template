import streamlit as st
from auth.auth import logout


logout()
st.rerun()
