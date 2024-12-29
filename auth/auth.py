import os

import requests
import streamlit as st
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

load_dotenv()


# Initialize OAuth (example with Google OAuth)
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")


# OAuth 2.0 Client Configuration
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]


def get_user_info(credentials):
    """Fetch user info using Google's API."""
    response = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {credentials.token}"},
    )
    return response.json()


def credentials_to_dict(credentials):
    """Converts credentials object to a dictionary for session storage."""
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


def create_flow():
    """Create a Google OAuth flow using environment variables."""

    return Flow.from_client_config(
        client_config={
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI],
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )


def login_button():
    """Start the login process by generating the Google OAuth URL."""
    flow = create_flow()
    auth_url, _ = flow.authorization_url(prompt="consent")

    # this part is needed because google blocks redirect in iframes and I want to avoid opening a new tab
    st.button("Login with Google", on_click=lambda: st.session_state.update({"login_click": "1"}))
    if st.session_state.get('login_click') == '1':
        st.write(
            f'''
            <meta http-equiv="refresh" content="0; url={auth_url}">
            ''',
            unsafe_allow_html=True,
        )
        st.session_state.update({'login_click': '0'})


def handle_oauth_callback():
    """Handle the OAuth callback and update session state."""
    flow = create_flow()

    # Extract the authorization code from the URL
    query_params = st.query_params
    if "code" in query_params:
        code = query_params["code"]
        try:
            flow.fetch_token(code=code)
            credentials = flow.credentials
            st.session_state.credentials = credentials_to_dict(credentials)
            st.session_state.user = get_user_info(credentials)

            # Clear query parameters after successful login
            st.query_params.clear()

            # Redirect to the reserved area
            st.session_state["page"] = "reserved_area"
            st.success(f"Successfully logged in as {st.session_state.user['name']}!")

            # Force Streamlit to rerun and navigate to the new page
            st.rerun()
        except Exception as e:
            st.error(f"Login failed: {e}")


def logout():
    """Logout user"""
    st.query_params.clear()
    st.session_state.pop("user", None)
    st.session_state.pop("sub_page", None)
    st.session_state.update({'page': 'homepage'})
    st.success(f"Successfully logged out!")
