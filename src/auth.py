import os
import logging
import requests
import streamlit as st
from streamlit_oauth import OAuth2Component
from constants import SessionState

logger = logging.getLogger(__name__)

class Authenticate:

    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    AUTHORIZE_URL = os.environ.get('AUTHORIZE_URL')
    TOKEN_URL = os.environ.get('TOKEN_URL')
    REFRESH_TOKEN_URL = os.environ.get('REFRESH_TOKEN_URL')
    REVOKE_TOKEN_URL = os.environ.get('REVOKE_TOKEN_URL')
    REDIRECT_URI = os.environ.get('REDIRECT_URI')
    SCOPE = os.environ.get('SCOPE')
    USERINFO_URL = os.environ.get('USERINFO_URL')

    oauth2 = None

    def __init__(self):
        """ Initialize the component
        """
        self.oauth2 = OAuth2Component(self.CLIENT_ID,
                                      self.CLIENT_SECRET,
                                      self.AUTHORIZE_URL,
                                      self.TOKEN_URL,
                                      self.REFRESH_TOKEN_URL,
                                      self.REVOKE_TOKEN_URL)

    def get_token(self):
        """ Gets the OAuth token associated with the user from the last authentication
            session.
            
            Returns: OAuth Token
        """
        if not SessionState.TOKEN in st.session_state:
            logger.debug("User not logged in.  Cannot retrieve token.")
            return None
        
        full_token = st.session_state[SessionState.TOKEN]
        if full_token != None:
            token = full_token["access_token"]
            logger.debug("Token: %s. Full Token: %s", token, full_token)
            return token

    def get_username(self):
        """ Gets the username of the currently authenticated user.
        
            Returns: Username
        """
        if not self.is_logged_in():
            logger.error("User not logged in.  Cannot retrieve token.")
            return None

        if not SessionState.USERNAME in st.session_state:
            msg = "User apparently logged in without a username."
            logger.error(msg)
            raise ValueError(msg)

        username = st.session_state[SessionState.USERNAME]
        if username is None or len(username) == 0:
            msg = "Username from session is null or empty!"
            logger.error(msg)
            raise ValueError(msg)

        return username            

    def is_logged_in(self):
        """ Checks to see if the user is currently loggred in.
        
            Returns: True if the user is authenticated 
        """
        token = self.get_token()
        if token is not None and len(token) > 0:
            return True

    def retrieve_user_info(self, bearer_token):
        """ Retrieves the username from OpenShift associated with the session.
        
            bearer_token - oauth2 token

            Returns: username
        """
        # ensure the user is logged in
        if bearer_token is None or len(bearer_token) == 0:
            msg = "Bearer Token is null or empty.  Cannot get userinfo until authenticated."
            logger.error(msg)
            raise ValueError(msg)

        # invoke the userinfo endpoint
        headers = {
            "Authorization": f"Bearer {bearer_token}"
        }
        response = requests.get(self.USERINFO_URL, headers=headers)
        if response.status_code != 200:
            msg = f"Unable to retrieve userinfo from OpenShift.  Code={response.status_code} Msg={response.text}"
            logger.error(msg)
            raise ValueError(msg)

        # extract info from response
        response_json = response.json()
        logger.info("User Info from OpenShift: %s", response_json)
        username = response_json["metadata"]["name"]
        logger.info("Username of authenticated user: %s", username)
        return username

    def verify_authenticate_response(self, result):
        """ Authenticates a response from the oauth authenticate button.
        
            result - authentication action response
        """
        if result and 'token' in result:
            logger.debug("Authentication successful!  %s", result)

            # Gather all the user info before persisting the token info (no partials)
            full_token = result.get('token')
            token = full_token["access_token"]
            username = self.retrieve_user_info(token)

            # save authentication info in session
            st.session_state[SessionState.TOKEN] = full_token
            st.session_state[SessionState.USERNAME] = username

            return True
        else:
            return False

    def logout(self):
        """ Logs the current user out of the system. """
        del st.session_state[SessionState.TOKEN]
        del st.session_state[SessionState.USERNAME]
        st.rerun()
