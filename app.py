import streamlit as st
from auth.auth import login, authenticator
from pages import page1, page2, page3

# Pages
st.set_page_config(page_title="App Template", layout="wide", initial_sidebar_state="collapsed")


def homepage():
    st.title("Welcome to the App")
    st.write("This is a template app. Feel free to explore!")
    st.markdown("[Register/Login](#reserved-area)")


def reserved_area():
    st.title("Reserved Area")
    user = st.session_state.get("user")
    if not user:
        st.warning("You must log in to access this area.")
        login()
    else:
        st.success(f"Welcome, {user['name']}!")
        menu = ["Page 1", "Page 2", "Page 3"]
        choice = st.sidebar.selectbox("Navigate", menu)
        if choice == "Page 1":
            page1.display()
        elif choice == "Page 2":
            page2.display()
        elif choice == "Page 3":
            page3.display()


# Routing

if "page" not in st.session_state:
    st.session_state["page"] = "homepage"


# Sidebar navigation
def sidebar_menu():
    st.sidebar.button("Go to Homepage", on_click=lambda: st.session_state.update({"page": "homepage"}))
    if st.session_state.get("user"):
        st.sidebar.button("Go to Reserved Area", on_click=lambda: st.session_state.update({"page": "reserved_area"}))
        st.sidebar.markdown("### Pages")
        st.sidebar.button("Page 1", on_click=lambda: st.session_state.update({"page": "reserved_area"}))
        st.sidebar.button("Page 2", on_click=lambda: st.session_state.update({"page": "reserved_area"}))
        st.sidebar.button("Page 3", on_click=lambda: st.session_state.update({"page": "reserved_area"}))
    else:
        st.sidebar.button("Go to Reserved Area", on_click=lambda: st.session_state.update({"page": "reserved_area"}))


# Remove default page header
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] { display: none; }
    </style>
    """,
    unsafe_allow_html=True
)


sidebar_menu()


if st.session_state["page"] == "homepage":
    homepage()
elif st.session_state["page"] == "reserved_area":
    reserved_area()
