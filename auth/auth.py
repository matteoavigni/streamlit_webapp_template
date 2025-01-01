import os
from time import sleep

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

    st.write(
        f'''
        <a href="{auth_url}" target="_blank" style="text-decoration:none;">
            <button style="padding: 10px 20px; font-size: 16px; background-color: #4285F4; color: white; border: none; border-radius: 5px; cursor: pointer;">
                Login with Google
            </button>
        </a>
        ''',
        unsafe_allow_html=True,
    )


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
            st.success(f"Successfully logged in as {st.session_state.user['name']}!")
            sleep(0.5)
            st.rerun()
        except Exception as e:
            st.error(f"Login failed: {e}")


def logout():
    """Logout user"""
    st.session_state.clear()  # Clear all session state variables
    homepage_url = "/"  # Adjust this based on your Streamlit deployment path
    st.markdown(
        f"""
        <meta http-equiv="refresh" content="0;url={homepage_url}">
        """,
        unsafe_allow_html=True,
    )
    st.success(f"Successfully logged out!")  # TODO: this is not shown
    st.stop()  # Prevent further execution of the script
