"""
User Activity Tab for Admin Panel
Handles user activity monitoring and logs
"""

import streamlit as st
from auth_login.database import AuthenticationManager


class UserActivityTab:
    """User Activity Tab - Monitor user activities and system usage"""
    
    def __init__(self, auth_manager: AuthenticationManager):
        """
        Initialize User Activity tab
        
        Args:
            auth_manager: AuthenticationManager instance for database operations
        """
        self.auth = auth_manager
    
    def render(self):
        """Render the User Activity tab"""
        st.markdown('''
            <div class="content-card">
                <h2>📊 User Activity</h2>
                <p>Monitor user activities and system usage.</p>
                <br>
                <p style="color: #9ca3af;">Coming soon: Activity logs, login history, usage statistics...</p>
            </div>
        ''', unsafe_allow_html=True)
