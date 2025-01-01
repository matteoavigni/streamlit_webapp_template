import streamlit as st
from auth.auth import logout


def is_logged_in():
    if st.session_state.get("user"):
        return True
    else:
        return False


def permission_denied():
    st.error("This page is not accessible for non authenticated users!")
    st.markdown("""
    <a href="app" target="_self">Go to the homepage</a>
    """, unsafe_allow_html=True)


def sidebar_menu():
    # Remove default page header
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] { display: none; }
        </style>
        """,
        unsafe_allow_html=True
    )

    # update sidebar menu
    go_to_homepage_button = st.sidebar.button("Homepage")
    go_to_reserved_area_button = st.sidebar.button("Reserved Area")
    if st.session_state.get("user"):

        st.sidebar.markdown("### Pages")
        name = st.sidebar.button("Name")
        profile_picture = st.sidebar.button("Profile Picture")
        email = st.sidebar.button("Email")
        st.sidebar.button("Logout", on_click=lambda: logout())

        if name:
            st.switch_page("pages/01_Name.py")
        elif profile_picture:
            st.switch_page("pages/02_Profile_Picture.py")
        elif email:
            st.switch_page("pages/03_Email.py")

    if go_to_homepage_button:
        st.session_state.update({"page": 'homepage'})
        st.switch_page("app.py")
    elif go_to_reserved_area_button:
        st.session_state.update({"page": 'reserved_area'})
        st.switch_page("app.py")
