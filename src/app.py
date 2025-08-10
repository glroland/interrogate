import logging
import streamlit as st
from auth import Authenticate
from home import HomePageView

logger = logging.getLogger(__name__)

# Setup Logging
logging.basicConfig(level=logging.DEBUG,
    handlers=[
        # no need from a docker container - logging.FileHandler("interrogate.log"),
        logging.StreamHandler()
    ])

st.title('Interrogate My Docs')

authenticate = Authenticate()
authenticate.render()

if authenticate.is_logged_in():
    home_page_view = HomePageView(authenticate)
    home_page_view.render()
