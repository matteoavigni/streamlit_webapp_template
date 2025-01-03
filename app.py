import streamlit as st
from utils import is_logged_in

if st.session_state.get('logged_out', False):
    st.success(f"Successfully logged out!")
    st.session_state.logged_out = False  # reset logged_out value

login_page = st.Page('pages/auth/login.py', title="Log in", icon=":material/login:")
logout_page = st.Page('pages/auth/logout.py', title="Log out", icon=":material/logout:")
processing_login = st.Page("pages/auth/processing_login.py", title="Processing Login", icon="⏳")

homepage = st.Page("pages/homepage.py", title="Homepage", icon="🏠")
reserved_area = st.Page("pages/reserved_area.py", title="Reserved Area", icon=":material/dashboard:")

profile_info = st.Page("pages/profile_info.py", title="Show Profile", icon="👤")
show_name = st.Page("pages/show_name.py", title="Show Name", icon="👉")
show_email = st.Page("pages/show_email.py", title="Show Email", icon="✉️")
show_profile_picture = st.Page("pages/show_profile_picture.py", title="Show Profile Picture", icon="📷")

if is_logged_in():
    pg = st.navigation(
        {
            "Menu": [homepage, reserved_area],
            "Reserved Area Apps": [show_name, show_email, show_profile_picture],
            "Account": [profile_info, logout_page],
        }
    )

elif "code" in st.query_params:
    pg = st.navigation([processing_login])
else:
    pg = st.navigation([homepage, login_page])

pg.run()

# check if reserved_area is in the query
if 'reserved_area' == st.query_params.get('page'):
    st.query_params.pop('page')  # remove the 'page' query param
    st.switch_page(reserved_area)
