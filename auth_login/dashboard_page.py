import streamlit as st
import sys
import os
import time
from typing import Dict, List, Optional
from auth_login.database import AuthenticationManager


class DashboardManager:
    """Handles dashboard data and business logic"""
    
    def __init__(self):
        self.auth = AuthenticationManager()
    
    def get_dashboard_metrics(self) -> Dict[str, Dict]:
        """Get dashboard metrics - currently returns mock data"""
        # TODO: Replace with actual database queries when tables are available
        return {
            'organizations': {
                'value': 325456,
                'change': '5%',
                'label': 'SINCE LAST MONTH',
            },
            'pipelines': {
                'value': 3006,
                'change': '-4.54%',
                'label': 'SINCE LAST MONTH',
            },
            'terminals': {
                'value': '60%',
                'change': '2.64%',
                'label': 'SINCE LAST MONTH',
            },
            'assets': {
                'value': 852,
                'change': '6.84%',
                'label': 'SINCE LAST MONTH',
            }
        }
    
    def get_user_info(self, user_id: int) -> Optional[Dict]:
        """Get user information"""
        return self.auth.get_user_by_id(user_id)
    
    def close(self):
        """Close database connection"""
        self.auth.close_pool()


class DashboardPage:
    """Handles dashboard page UI and rendering"""
    
    def __init__(self):
        """Initialize dashboard page"""
        self.dashboard_manager = DashboardManager()
    
    def _render_sidebar(self):
        """Render sidebar with welcome message and admin controls"""
        with st.sidebar:
            user = st.session_state.get('user', {})
            username = user.get('username', 'User')
            is_admin = user.get('is_admin', False)
            
            st.title("Values 360")
            st.markdown(f"👋 Welcome, **{username}**")
            st.markdown("---")
            
            # Admin Controls - Only show if user is admin
            if is_admin:
                st.subheader("🔒 Admin Controls")
                
                # Admin Panel Button
                if st.button("⚙️ Admin Panel", key="admin_panel_btn", use_container_width=True):
                    st.session_state.current_page = "admin_panel"
                    st.rerun()
                
                st.divider()
            
            # Navigation Section
            st.subheader("📋 Navigation")
            
            # Main Dashboard Box
            if st.button("📈 Main Dashboard", key="main_dashboard", use_container_width=True):
                st.session_state.current_page = "main_dashboard"
                st.rerun()
            
            # Form Assessment Box
            if st.button("📋 Form Assessment", key="form_assessment", use_container_width=True):
                st.session_state.current_page = "form_assessment"
                st.rerun()
            
            # Assessment Box
            if st.button("✅ Assessment", key="assessment", use_container_width=True):
                st.session_state.current_page = "assessment"
                st.rerun()
            
            st.markdown("---")
            
            # Logout button
            if st.button("🚪 Logout", type="primary", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.session_state.user_id = None
                st.rerun()
    
    def _render_metrics(self):
        """Render dashboard metrics using Streamlit columns"""
        metrics = self.dashboard_manager.get_dashboard_metrics()
        
        # Create 4 columns for the metric cards
        cols = st.columns(4)
        
        for idx, (key, data) in enumerate(metrics.items()):
            title = key.replace('_', ' ').title()
            
            with cols[idx]:
                with st.container(border=True):
                    st.metric(
                        label=title,
                        value=data['value'],
                        delta=data['change']
                    )
    
    def render(self):
        """Render the complete dashboard page"""
        st.set_page_config(
            page_title="Valve 360 - Dashboard",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Render sidebar
        self._render_sidebar()
        
        # App Header with Valve 360 title
        st.title("Valve 360 Dashboard")
        
        # Create tabs
        tab1, tab2 = st.tabs(["📊 Data Management", "🔍 Entity Overview"])
        
        with tab1:
            # Data Management Tab - Show metric cards
            st.subheader("Key Metrics")
            self._render_metrics()
        
        with tab2:
            # Entity Overview Tab - Blank for now
            st.info("Entity Overview - Coming soon...")
        
        # Additional spacing
        st.markdown("<br><br>", unsafe_allow_html=True)


class DashboardApp:
    """Main dashboard application class"""
    
    def __init__(self):
        """Initialize the dashboard app"""
        self.dashboard_page = DashboardPage()
    
    def run(self):
        """Run the dashboard app"""
        # Check if user is logged in
        if not st.session_state.get('logged_in', False):
            st.error("Please login to access the dashboard")
            st.stop()
        
        self.dashboard_page.render()


# ==================== MAIN ENTRY POINT ====================

if __name__ == "__main__":
    app = DashboardApp()
    app.run()
