import streamlit as st

# Set page title
st.set_page_config(page_title="Simple Streamlit App", layout="centered")

# App title
title = st.title("Welcome to My Streamlit App 👋")

# User input
name = st.text_input("Enter your name:", "")

# Display greeting message
if name:
    st.success(f"Hello, {name*5}! Welcome to this Streamlit app. 😊")
else:
    st.info("Please enter your name above.")

# Button example
if st.button("Click Me!"):
    st.write("You clicked the button! 🎉")
    title = st.title("New Title!")
