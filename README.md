# stramlit_webapp_template

Teamplate for a Python WebApp built with Streamlit.

There's a homepage and a reserved area accessible after login.

The login can be done using the Google account through OAuth2.0.


## Setup:
1. Clone the project
2. Activate the Google authentication API: https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid
3. Add the `.env` file in the project folder specifying the variables below:

```
GOOGLE_CLIENT_ID='your google client ID'
GOOGLE_CLIENT_SECRET='your google client secret'
REDIRECT_URI='redirect URI, es, in local http://localhost:8501. note that this must be added to the authorized URIs in the Google Credentials app'
GOOGLE_CLIENT_CONFIG='JSON as in the Google Client Configuration file'
```
4. Install streamlit: https://docs.streamlit.io/get-started/installation
5. Run the app:

```bash
streamlit run app.py
```
