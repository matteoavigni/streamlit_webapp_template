import streamlit as st
from auth.auth import login_button, handle_oauth_callback
from utils import sidebar_menu

# Pages
st.set_page_config(page_title="App Template", layout="wide", initial_sidebar_state="collapsed")


def homepage():
    st.title("Welcome to the App")
    st.write("This is a template app. Feel free to explore!")
    if st.session_state.get("user"):
        st.button("Go to Reserved Area", on_click=lambda: st.session_state.update({"page": "reserved_area"}),
                  key='go_to_reserved')
    else:
        st.button("Login to Access Reserved Area", on_click=lambda: st.session_state.update({"page": "reserved_area"}),
                  key='go_to_reserved_when_credentials_are_missing')


def reserved_area():
    st.title("Reserved Area")

    if "user" not in st.session_state:
        st.warning("You must log in to access this area.")
        login_button()
    else:
        user = st.session_state.user
        st.write(f"Welcome, {user['name']}!")

        st.markdown(
            "Here you will find a list pages built using [Streamlit](https://streamlit.io/):", unsafe_allow_html=True
        )

        name_home = st.button("Name", key='name_home')
        profile_picture_home = st.button("Profile Picture", key='profile_picture_home')
        email_home = st.button("Email", key='email_home')

        if name_home:
            st.switch_page("pages/01_Name.py")
        elif profile_picture_home:
            st.switch_page("pages/02_Profile_Picture.py")
        elif email_home:
            st.switch_page("pages/03_Email.py")


def oauth_callback():
    st.title("Processing Login")
    handle_oauth_callback()


# Routing
if "page" not in st.session_state:
    st.session_state["page"] = "homepage"


# Detect if the callback URL is accessed
query_params = st.query_params
if "code" in query_params and st.session_state.get("page") != "reserved_area":
    oauth_callback()
else:

    if st.session_state["page"] == "homepage":
        homepage()
    elif st.session_state["page"] == "reserved_area":
        reserved_area()
    sidebar_menu()
