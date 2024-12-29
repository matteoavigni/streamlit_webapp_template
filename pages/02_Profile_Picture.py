import streamlit as st
from utils import permission_denied
from utils import sidebar_menu


def display():
    st.title("Image")
    st.write("See below your profile picture!")
    st.image(st.session_state.user['picture'],
             caption=f"Google profile picture for {st.session_state.user['name']}",
             width=400)


if "user" in st.session_state:
    display()
else:
    permission_denied()
sidebar_menu()
