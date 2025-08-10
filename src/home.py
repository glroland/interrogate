import streamlit as st
from auth import Authenticate
from files import FileGateway

class HomePageView:
    """ Home Page View """

    authenticate = None
    file_gateway = None

    def __init__(self, authenticate: Authenticate):
        """ Initialize the component
        
            authenticate - authenticate component 
        """
        self.authenticate = authenticate
        self.file_gateway = FileGateway()

    def render(self):
        username = self.authenticate.get_username()

        st.write(f"Welcome! {username}")

        # List files for user
        files = self.file_gateway.list(username)
        if files is None or len(files) == 0:
            st.write("No files for user.")
        else:
            for file in files:
                st.write(file)
            st.write(f"{len(files)} files found for user.")
