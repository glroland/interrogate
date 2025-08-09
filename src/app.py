import streamlit as st

# Set the title of the app
st.title('My First Streamlit App')

# Add a simple text message
st.write('Welcome to your new Streamlit application!')

# Add a text input widget
user_name = st.text_input('What is your name?', 'Guest')

# Display a personalized greeting
st.write(f'Hello, {user_name}!')

# Add a button
if st.button('Click Me!'):
    st.write('Button clicked!')
