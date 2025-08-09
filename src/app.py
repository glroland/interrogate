import streamlit as st
from streamlit_oauth import OAuth2Component
import os
import requests

username = "GUEST"

# Retrieve credentials from environment variables
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
AUTHORIZE_URL = os.environ.get('AUTHORIZE_URL')
TOKEN_URL = os.environ.get('TOKEN_URL')
REFRESH_TOKEN_URL = os.environ.get('REFRESH_TOKEN_URL')
REVOKE_TOKEN_URL = os.environ.get('REVOKE_TOKEN_URL')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
SCOPE = os.environ.get('SCOPE')
USERINFO_URL = os.environ.get('USERINFO_URL')

oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)

# Check if token exists in session state
if 'token' not in st.session_state:
    # If not, show authorize button
    result = oauth2.authorize_button("Authorize", REDIRECT_URI, SCOPE)
    if result and 'token' in result:
        # If authorization successful, save token in session state
        st.session_state.token = result.get('token')
        st.rerun()
else:
    # If token exists in session state, show the token
    token = st.session_state['token']
    st.json(token)
    if st.button("Refresh Token"):
        # If refresh token button is clicked, refresh the token
        token = oauth2.refresh_token(token)
        st.session_state.token = token
        st.rerun()

    bearer_token = token["access_token"]
    st.write(bearer_token)
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    response = requests.get(USERINFO_URL, headers=headers)
    if response.status_code == 200:
        print("Request successful!")
        response_json = response.json()
        print(response_json)  # Assuming the response is JSON
        username = response_json["metadata"]["name"]
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)

    if st.button("Logout"):
        del st.session_state["token"]
        st.rerun()

st.markdown(f"Welcome! {username}")

# Set the title of the app
st.title('My First Streamlit App')

# Add a simple text message
st.write('Welcome to your new Streamlit application!')

# Add a text input widget
user_name = st.text_input('What is your name?', f'{username}')

# Display a personalized greeting
st.write(f'Hello, {user_name}!')

# Add a button
if st.button('Click Me!'):
    st.write('Button clicked!')

st.write(st.user)
