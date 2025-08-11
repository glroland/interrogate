import logging
import streamlit as st
from auth import Authenticate
from files import FileGateway
from constants import SessionState

logger = logging.getLogger(__name__)

# Setup Logging
logging.basicConfig(level=logging.DEBUG,
    handlers=[
        # no need from a docker container - logging.FileHandler("interrogate.log"),
        logging.StreamHandler()
    ])

st.title('Interrogate My Docs')

# Authenticate
authenticate = Authenticate()
if not authenticate.is_logged_in():
    result = authenticate.oauth2.authorize_button("Login via OpenShift",
                                            authenticate.REDIRECT_URI,
                                            authenticate.SCOPE)
    if authenticate.verify_authenticate_response(result):
        st.rerun()

# Require authentication
if authenticate.is_logged_in():
    username = authenticate.get_username()

    # Get user's file list
    file_gateway = FileGateway()
    files = file_gateway.list(username)
    file_checkboxes = {}

    # Display file selections
    with st.sidebar:
        # Welcome User
        st.header(f"Welcome, {username}!")

        # Display Logout Button
        if st.button("Logout"):
            authenticate.logout()

        # List files for user
        st.subheader("Your Files:")
        if files is None or len(files) == 0:
            st.write("No files for user.")
        else:
            for file in files:
                checkbox = st.checkbox(file, value=True)
                file_checkboxes[file] = checkbox
            st.write(f"{len(files)} files found for user.")

    # Main UI View
    chat_input = st.chat_input("How can I help you with the selected files?")
