import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from auth_login.login_page import LoginApp
from auth_login.dashboard_page import DashboardApp
from admin_panel import AdminPanelApp

def main():
    """Main entry point for the Streamlit app"""
    # st.set_page_config must be the first Streamlit command
    st.set_page_config(
            page_title="Valve 360",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
    
    # Initialize session state
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.user_id = None
        st.session_state.current_page = None
    
    # Route to appropriate page based on login status and current_page
    if not st.session_state.logged_in:
        # User not logged in - show login page
        login = LoginApp()
        login.run()
    else:
        # User logged in - check which page to show
        current_page = st.session_state.get('current_page', 'dashboard')
        
        if current_page == 'admin_panel':
            # Show admin panel
            admin_panel = AdminPanelApp()
            admin_panel.run()
        else:
            # Show dashboard (default)
            dashboard = DashboardApp()
            dashboard.run()

if __name__ == "__main__":
    main()