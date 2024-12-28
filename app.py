import streamlit as st
from auth.auth import logout, login_button, handle_oauth_callback
from pages import page1, page2, page3

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
        st.write(user)

        if 'sub_page' in st.session_state:
            if st.session_state['sub_page'] == "page1":
                page1.display()
            elif st.session_state['sub_page'] == "page2":
                page2.display()
            elif st.session_state['sub_page'] == "page3":
                page3.display()


def oauth_callback():
    st.title("Processing Login")
    handle_oauth_callback()


# Routing
if "page" not in st.session_state:
    st.session_state["page"] = "homepage"


# Sidebar navigation
def sidebar_menu():
    st.sidebar.button("Homepage", on_click=lambda: st.session_state.update({"page": "homepage",
                                                                            "sub_page": None}))
    st.sidebar.button("Reserved Area", on_click=lambda: st.session_state.update({"page": "reserved_area",
                                                                                 "sub_page": None}))
    if st.session_state.get("user"):

        st.sidebar.markdown("### Pages")
        st.sidebar.button("Page 1", on_click=lambda: st.session_state.update({"sub_page": "page1"}))
        st.sidebar.button("Page 2", on_click=lambda: st.session_state.update({"sub_page": "page2"}))
        st.sidebar.button("Page 3", on_click=lambda: st.session_state.update({"sub_page": "page3"}))
        st.sidebar.button("Logout", on_click=lambda: logout())


# Remove default page header
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] { display: none; }
    </style>
    """,
    unsafe_allow_html=True
)


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
