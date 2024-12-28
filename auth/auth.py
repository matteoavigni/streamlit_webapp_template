import os

import requests
import streamlit as st
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow

load_dotenv()


# Initialize OAuth (example with Google OAuth)
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")


# OAuth 2.0 Client Configuration
CLIENT_SECRETS_FILE = "client_secret.json"  # Ensure this file is downloaded from Google Cloud Console
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


def login_button():
    """Start the login process by generating the Google OAuth URL."""
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    auth_url, _ = flow.authorization_url(prompt="consent")
    st.write(
        f'''
        <a target="_self" href="{auth_url}">
            <button>Login with Google</button>
        </a>
        ''',
        unsafe_allow_html=True,
    )


def handle_oauth_callback():
    """Handle the OAuth callback and update session state."""
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )

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
