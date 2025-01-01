import streamlit as st
from utils import permission_denied


if "user" in st.session_state:
    st.title("Image")
    st.write("See below your profile picture!")
    st.image(st.session_state.user['picture'],
             caption=f"Google profile picture for {st.session_state.user['name']}",
             width=400)
else:
    permission_denied()
