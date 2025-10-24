import streamlit as st

st.set_page_config(
    page_title="Welcome Page",  
    page_icon="🏠",         
)

# WELCOME PAGE TITLE
st.title("Welcome to your personal steps data! 📊")

# INTRODUCTORY TEXT
st.write("""
You can navigate to the different pages using the sidebar on the left.

### How to use this app:
- **Survey**: Come answer some quick questions about your steps!
- **Visuals Page**: Go here to see your steps visualized in different graphs.

This website is part of Kathy Do's CS 1301 Lab 2.
""")

