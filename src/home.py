import streamlit as st
from auth import Authenticate

class HomePageView:
    """ Home Page View """

    authenticate = None

    def __init__(self, authenticate: Authenticate):
        """ Initialize the component
        
            authenticate - authenticate component 
        """
        self.authenticate = authenticate

    def render(self):
        username = self.authenticate.get_username()

        st.write(f"Welcome! {username}")

        # Add a text input widget
        user_name = st.text_input('What is your name?', f'{username}')

        # Display a personalized greeting
        st.write(f'Hello, {user_name}!')

        # Add a button
        if st.button('Click Me!'):
            st.write('Button clicked!')
