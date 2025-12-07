import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from auth_login.login_page import LoginApp
from auth_login.dashboard_page import DashboardApp

def main():
    """Main entry point for the Streamlit app"""
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.user_id = None
    
    # Route to appropriate page based on login status
    if st.session_state.logged_in:
        dashboard = DashboardApp()
        dashboard.run()
    else:
        login = LoginApp()
        login.run()

if __name__ == "__main__":
    main()