import streamlit as st


def display():
    st.title("Image")
    st.write("See below your profile picture!")
    st.image(st.session_state.user['picture'],
             caption=f"Google profile picture for {st.session_state.user['name']}",
             width=400)
