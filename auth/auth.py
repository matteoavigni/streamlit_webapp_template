import streamlit as st
from oauthlib.oauth2 import WebApplicationClient
import requests
import os

# Initialize OAuth (example with Google OAuth)
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
client = WebApplicationClient(CLIENT_ID)


def login():
    """Generate the Google OAuth login URL and display it."""
    authorization_endpoint = "https://accounts.google.com/o/oauth2/auth"
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=REDIRECT_URI,
        scope=["openid", "email", "profile"],
    )
    st.write(f"[Login with Google]({request_uri})")


def handle_callback():
    """Handle the OAuth callback to retrieve user information."""
    # Extract the authorization code from query params
    query_params = st.experimental_get_query_params()
    code = query_params.get("code", [None])[0]

    if not code:
        st.error("Authorization code not found in the callback URL.")
        return False

    # Exchange authorization code for an access token
    token_endpoint = "https://oauth2.googleapis.com/token"
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        redirect_url=REDIRECT_URI,
        code=code,
        client_secret=CLIENT_SECRET,
    )
    token_response = requests.post(token_url, headers=headers, data=body)
    client.parse_request_body_response(token_response.text)

    # Retrieve user information
    userinfo_endpoint = "https://openidconnect.googleapis.com/v1/userinfo"
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.status_code == 200:
        user_info = userinfo_response.json()
        # Save user info in session state
        st.session_state["user"] = {
            "name": user_info.get("name"),
            "email": user_info.get("email"),
        }
        # Clear query parameters and refresh the app
        st.experimental_set_query_params()
        st.experimental_rerun()
        return True
    else:
        st.error("Failed to fetch user information.")
        return False


def authenticator():
    """Check if the user is authenticated, and redirect to login if not."""
    if "user" not in st.session_state:
        if "code" in st.experimental_get_query_params():
            handle_callback()
        else:
            st.warning("You must log in to access this area.")
            login()
