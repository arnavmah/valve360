"""
Admin Panel Main Orchestrator
Coordinates all admin panel components and handles navigation
"""

import streamlit as st
from auth_login.database import AuthenticationManager
from admin_panel.user_management import UserManagementTab
from admin_panel.access_control import AccessControlTab
from admin_panel.user_activity import UserActivityTab


class AdminPanelPage:
    """Handles admin panel page UI and rendering"""
    
    def __init__(self):
        """Initialize admin panel page"""
        self.auth_manager = AuthenticationManager()
        
        # Initialize tab components
        self.user_management = UserManagementTab(self.auth_manager)
        self.access_control = AccessControlTab(self.auth_manager)
        self.user_activity = UserActivityTab(self.auth_manager)
        
        # Initialize session state for current section
        if 'admin_section' not in st.session_state:
            st.session_state.admin_section = 'view_assessment'
    
    def _render_sidebar(self):
        """Render sidebar with navigation"""
        with st.sidebar:
            user = st.session_state.get('user', {})
            username = user.get('username', 'User')
            
            st.markdown(f"# 👋 Welcome")
            st.markdown(f"### {username}")
            st.markdown("---")
            
            # Navigation Section
            st.markdown("### 📋 Go to")
            
            # View Assessment Button
            if st.button("📊 View Assessment", key="view_assessment_btn", use_container_width=True):
                st.session_state.admin_section = 'view_assessment'
                st.rerun()
            
            # New Assignment Button
            if st.button("➕ New Assignment", key="new_assignment_btn", use_container_width=True):
                st.session_state.admin_section = 'new_assignment'
                st.rerun()
            
            st.markdown("---")
            
            # Back to Dashboard button
            if st.button("🏠 Back to Dashboard", type="primary", key="back_to_dashboard"):
                st.session_state.current_page = "dashboard"
                st.rerun()
            
            # Logout button
            if st.button("🚪 Logout", type="primary"):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.session_state.user_id = None
                st.session_state.current_page = None
                st.session_state.admin_section = None
                st.rerun()
    
    def _render_view_assessment(self):
        """Render View Assessment section with tabs"""
        # Create tabs for different assessment views
        tab1, tab2, tab3 = st.tabs(["👥 User Management", "🔐 Access Control", "📊 User Activity"])
        
        with tab1:
            self.user_management.render()
        
        with tab2:
            self.access_control.render()
        
        with tab3:
            self.user_activity.render()
    
    def _render_new_assignment(self):
        """Render New Assignment section"""
        st.header("➕ New Assignment")
        st.write("This section will allow you to create new assignments.")
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("Coming soon: Assignment creation form...")
    
    def render(self):
        """Render the complete admin panel page"""
        st.set_page_config(
            page_title="Valve 360 - Admin Panel",
            page_icon="⚙️",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Render sidebar
        self._render_sidebar()
        
        # App Header
        st.title("⚙️ Admin Panel")
        
        # Render content based on selected section
        current_section = st.session_state.get('admin_section', 'view_assessment')
        
        if current_section == 'view_assessment':
            self._render_view_assessment()
        elif current_section == 'new_assignment':
            self._render_new_assignment()
        
        # Additional spacing
        st.markdown("<br><br>", unsafe_allow_html=True)


class AdminPanelApp:
    """Main admin panel application class"""
    
    def __init__(self):
        """Initialize the admin panel app"""
        self.admin_panel_page = AdminPanelPage()
    
    def run(self):
        """Run the admin panel app"""
        # Check if user is logged in and is admin
        if not st.session_state.get('logged_in', False):
            st.error("Please login to access the admin panel")
            st.stop()
        
        user = st.session_state.get('user', {})
        if not user.get('is_admin', False):
            st.error("Access denied. Admin privileges required.")
            st.stop()
        
        self.admin_panel_page.render()


# ==================== MAIN ENTRY POINT ====================

if __name__ == "__main__":
    app = AdminPanelApp()
    app.run()
