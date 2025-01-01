import time

import streamlit as st
from utils import is_logged_in


if st.session_state.get('welcome_user', False):
    st.success(f"Successfully logged in as {st.session_state.user['name']}!")
    st.session_state.welcome_user = False

st.markdown("""
# Reserved Area Homepage

## Welcome to the reserved area of this App. This section is accessible after login only

""")


if not is_logged_in():
    st.error("You must login to access this area. Redirecting to the homepage...")
    time.sleep(2)
    st.switch_page('pages/homepage.py')
else:
    given_name = st.session_state.get("user")['given_name']
    st.markdown(f"""
    Hello {given_name}, here you will find a list pages built using [Streamlit](https://streamlit.io/):
    """, unsafe_allow_html=True
    )
    st.page_link("pages/show_name.py", label="Show Name", icon="👉")
    st.page_link("pages/show_email.py", label="Show Email", icon="✉️")
    st.page_link("pages/show_profile_picture.py", label="Show Profile Picture", icon="📷")
