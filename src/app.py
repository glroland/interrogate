import logging
import streamlit as st
from auth import Authenticate

logger = logging.getLogger(__name__)

# Setup Logging
logging.basicConfig(level=logging.DEBUG,
    handlers=[
        # no need from a docker container - logging.FileHandler("interrogate.log"),
        logging.StreamHandler()
    ])

st.title('Interrogate Application')

authenticate = Authenticate()
authenticate.render()

if authenticate.is_logged_in():
    username = authenticate.get_username()

    st.write(f"Welcome! {username}")

    # Add a text input widget
    user_name = st.text_input('What is your name?', f'{username}')

    # Display a personalized greeting
    st.write(f'Hello, {user_name}!')

    # Add a button
    if st.button('Click Me!'):
        st.write('Button clicked!')
