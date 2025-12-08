import streamlit as st
import sys
import os
from typing import Dict, List, Optional
from auth_login.database import AuthenticationManager


class AdminPanelManager:
    """Handles admin panel data and business logic"""
    
    def __init__(self):
        self.auth = AuthenticationManager()
    
    def get_assessments(self) -> List[Dict]:
        """Get all assessments - placeholder for now"""
        # TODO: Implement actual database query
        return []
    
    def get_user_info(self, user_id: int) -> Optional[Dict]:
        """Get user information"""
        return self.auth.get_user_by_id(user_id)
    
    def close(self):
        """Close database connection"""
        self.auth.close_pool()


class AdminPanelPage:
    """Handles admin panel page UI and rendering"""
    
    CSS_STYLES = """
    <style>
    /* Global Styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: #0f0f1e;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1 {
        color: #fff;
        font-size: 1.8em;
        font-weight: 700;
        padding: 10px 0;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 8px;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
        color: #fff;
        font-size: 1.2em;
        font-weight: 600;
        margin: 5px 0;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #ccc;
        font-size: 1em;
        margin: 5px 0;
    }
    
    /* Reduce spacing between sections */
    [data-testid="stSidebar"] hr {
        margin: 8px 0 !important;
    }
    
    /* Main Content */
    [data-testid="stMainBlockContainer"] {
        padding: 20px 40px !important;
    }
    
    /* App Header with Gradient */
    .app-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 25px 35px;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.2);
        text-align: center;
    }
    
    .app-header h1 {
        color: #fff;
        font-size: 2.2em;
        font-weight: 700;
        margin: 0;
        font-family: 'Arial', 'Helvetica', sans-serif;
        text-shadow: none;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: none;
        color: #9ca3af;
        font-size: 0.95em;
        font-weight: 600;
        padding: 12px 24px;
        border-radius: 8px 8px 0 0;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(102, 126, 234, 0.2);
        color: #fff;
        border-bottom: 3px solid #667eea;
    }
    
    /* Section Headers with Grey Glow */
    [data-testid="stSidebar"] h3 {
        color: #e0e0e0;
        text-shadow: 0 0 5px rgba(224, 224, 224, 0.2);
        font-size: 1.1em;
        font-weight: 600;
        margin: 8px 0 8px 0;
    }
    
    /* Navigation Boxes - Compact */
    .stButton > button {
        background: #2a2a3e !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        padding: 6px 12px !important;
        margin: 4px 0 !important;
        color: #fff !important;
        font-size: 0.9em !important;
        font-weight: 500 !important;
        height: auto !important;
        min-height: 32px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: #3a3a4e !important;
        border-color: rgba(102, 126, 234, 0.5) !important;
        transform: translateX(3px) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Purple Styling for Back to Dashboard and Logout Buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #7a8ef0 0%, #8a5bb8 100%) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Content Card */
    .content-card {
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.9) 0%, rgba(22, 33, 62, 0.9) 100%);
        border-radius: 16px;
        padding: 30px;
        margin-top: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .content-card h2 {
        color: #fff;
        font-size: 1.8em;
        margin-bottom: 20px;
    }
    
    .content-card p {
        color: #ccc;
        font-size: 1em;
        line-height: 1.6;
    }
    
    /* Compact User Action Buttons - More specific targeting */
    [data-testid="stExpander"] .stButton > button {
        padding: 4px 6px !important;
        font-size: 0.9em !important;
        min-height: 28px !important;
        height: 28px !important;
        margin: 2px 0 !important;
    }
    </style>
    """
    
    def __init__(self):
        """Initialize admin panel page"""
        self.admin_manager = AdminPanelManager()
        self._apply_styles()
        # Initialize session state for current section
        if 'admin_section' not in st.session_state:
            st.session_state.admin_section = 'view_assessment'
    
    def _apply_styles(self):
        """Apply custom CSS styles"""
        st.markdown(self.CSS_STYLES, unsafe_allow_html=True)
    
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
            # User Management Tab
            st.markdown("## 👥 User Management")
            # st.markdown("Manage users, roles, and permissions.")
            # st.markdown("<br>", unsafe_allow_html=True)
            # Add User Button and Form
            # Limit form width
            col_form_left, col_form_center, col_form_right = st.columns([0.01, 0.98, 0.01])
            
            with col_form_center:
                with st.expander("➕ Add New User", expanded=False):
                    with st.form("add_user_form", clear_on_submit=True):
                        # Basic fields in 2 columns
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            username = st.text_input("Username *", placeholder="Enter username", key="new_username")
                            full_name = st.text_input("Full Name", placeholder="Enter full name", key="new_fullname")
                            phone_number = st.text_input("Phone Number", placeholder="Enter phone number", key="new_phone")
                        
                        with col2:
                            password = st.text_input("Password *", type="password", placeholder="Enter password", key="new_password")
                            email = st.text_input("Email", placeholder="Enter email address", key="new_email")
                            extra_notes = st.text_input("Extra Notes", placeholder="Additional info (optional)", key="new_extra")
                        
                        # Checkboxes and role assignment in one row
                        col3, col4 = st.columns(2)
                        with col3:
                            is_admin = st.checkbox("Admin Rights", key="new_admin")
                        with col4:
                            is_active = st.checkbox("Active", value=True, key="new_active")
                        
                        # Role assignment dropdown
                        try:
                            available_roles = self.admin_manager.auth.get_all_roles()
                            if available_roles:
                                role_options = {role['name']: role['id'] for role in available_roles}
                                selected_roles = st.multiselect(
                                    "Assign Roles",
                                    options=list(role_options.keys()),
                                    key="new_roles",
                                    help="Select one or more roles to assign to this user"
                                )
                            else:
                                selected_roles = []
                                st.info("No roles available. Create roles first.")
                        except Exception as e:
                            selected_roles = []
                            st.warning(f"Could not load roles: {str(e)}")
                        
                        # Submit button - centered and shorter
                        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
                        with col_btn2:
                            submitted = st.form_submit_button("Create User", type="primary", use_container_width=True)
                    
                    if submitted:
                        if not username or not password:
                            st.error("Username and Password are required!")
                        else:
                            try:
                                # Get current user ID for created_by field
                                current_user_id = st.session_state.get('user_id')
                                
                                # Create user with extra notes
                                new_user = self.admin_manager.auth.create_user(
                                    username=username,
                                    password=password,
                                    email=email if email else None,
                                    full_name=full_name if full_name else None,
                                    phone_number=phone_number if phone_number else None,
                                    is_admin=is_admin,
                                    created_by=current_user_id,
                                    extra=extra_notes if extra_notes else None
                                )
                                
                                if new_user:
                                    # Assign selected roles to the new user
                                    if selected_roles:
                                        for role_name in selected_roles:
                                            role_id = role_options[role_name]
                                            self.admin_manager.auth.assign_role_to_user(
                                                user_id=new_user['id'],
                                                role_id=role_id,
                                                assigned_by=current_user_id
                                            )
                                    
                                    st.success(f"✅ User '{username}' created successfully!")
                                    st.rerun()
                                else:
                                    st.error("Failed to create user. Please try again.")
                            except ValueError as e:
                                st.error(f"❌ {str(e)}")
                            except Exception as e:
                                st.error(f"❌ Error creating user: {str(e)}")
            
            st.markdown("---")
            
            # Display existing users grouped by roles
            st.markdown("### Existing Users")
            
            try:
                users = self.admin_manager.auth.get_all_users()
                all_roles = self.admin_manager.auth.get_all_roles()
                
                if users:
                    # Create a mapping of role_id -> list of users
                    users_by_role = {}
                    users_without_roles = []
                    
                    # Get roles for each user and organize them
                    for user in users:
                        user_roles = self.admin_manager.auth.get_user_roles(user['id'])
                        
                        if user_roles:
                            # User has roles - add to each role group
                            for role in user_roles:
                                role_name = role['name']
                                if role_name not in users_by_role:
                                    users_by_role[role_name] = []
                                users_by_role[role_name].append(user)
                        else:
                            # User has no roles
                            users_without_roles.append(user)
                    
                    # Display users grouped by role
                    # Wrap in same column structure as Add New User form
                    col_users_left, col_users_center, col_users_right = st.columns([0.01, 0.98, 0.01])
                    
                    with col_users_center:
                        for role in all_roles:
                            role_name = role['name']
                            if role_name in users_by_role:
                                st.markdown(f"#### 🔑 {role_name}")
                                
                                for user in users_by_role[role_name]:
                                    user_roles = self.admin_manager.auth.get_user_roles(user['id'])
                                    role_names = ", ".join([r['name'] for r in user_roles]) if user_roles else "None"
                                    
                                    # Expandable user card
                                    with st.expander(f"👤 {user.get('username')}", expanded=False):
                                        # Create two columns: info on left, buttons on right
                                        col_info, col_buttons = st.columns([3, 1])
                                        
                                        with col_info:
                                            # User details
                                            st.markdown(f"**ID:** {user.get('id')}")
                                            st.markdown(f"**Full Name:** {user.get('full_name') or 'N/A'}")
                                            st.markdown(f"**Email:** {user.get('email') or 'N/A'}")
                                            st.markdown(f"**Phone:** {user.get('phone_number') or 'N/A'}")
                                            
                                            # Status and Admin on one line
                                            status_text = "🟢 Active" if user.get('is_active') else "🔴 Inactive"
                                            admin_text = "✅ Yes" if user.get('is_admin') else "❌ No"
                                            st.markdown(f"**Status:** {status_text} &nbsp;&nbsp;&nbsp; **Admin:** {admin_text}")
                                            st.markdown(f"**Roles:** {role_names}")
                                        
                                        with col_buttons:
                                            # Action buttons stacked vertically on the right
                                            if st.button("✏️ Edit", key=f"edit_{user.get('id')}_role"):
                                                st.info(f"Edit functionality for {user.get('username')} - Coming soon")
                                            
                                            if st.button("🗑️ Deactivate", key=f"deactivate_{user.get('id')}_role"):
                                                try:
                                                    if self.admin_manager.auth.deactivate_user(user.get('id')):
                                                        st.success(f"User {user.get('username')} deactivated")
                                                        st.rerun()
                                                    else:
                                                        st.error("Failed to deactivate user")
                                                except Exception as e:
                                                    st.error(f"Error: {str(e)}")
                                
                                st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Display users without roles
                    if users_without_roles:
                        # Wrap in same column structure as Add New User form
                        col_norole_left, col_norole_center, col_norole_right = st.columns([0.01, 0.98, 0.01])
                        
                        with col_norole_center:
                            st.markdown("#### 👥 No Role Assigned")
                            
                            for user in users_without_roles:
                                # Expandable user card
                                with st.expander(f"👤 {user.get('username')}", expanded=False):
                                    # Create two columns: info on left, buttons on right
                                    col_info, col_buttons = st.columns([3, 1])
                                    
                                    with col_info:
                                        # User details
                                        st.markdown(f"**ID:** {user.get('id')}")
                                        st.markdown(f"**Full Name:** {user.get('full_name') or 'N/A'}")
                                        st.markdown(f"**Email:** {user.get('email') or 'N/A'}")
                                        st.markdown(f"**Phone:** {user.get('phone_number') or 'N/A'}")
                                        
                                        # Status and Admin on one line
                                        status_text = "🟢 Active" if user.get('is_active') else "🔴 Inactive"
                                        admin_text = "✅ Yes" if user.get('is_admin') else "❌ No"
                                        st.markdown(f"**Status:** {status_text} &nbsp;&nbsp;&nbsp; **Admin:** {admin_text}")
                                        st.markdown(f"**Roles:** None")
                                    
                                    with col_buttons:
                                        # Action buttons stacked vertically on the right
                                        if st.button("✏️ Edit", key=f"edit_{user.get('id')}_norole"):
                                            st.info(f"Edit functionality for {user.get('username')} - Coming soon")
                                        
                                        if st.button("🗑️ Deactivate", key=f"deactivate_{user.get('id')}_norole"):
                                            try:
                                                if self.admin_manager.auth.deactivate_user(user.get('id')):
                                                    st.success(f"User {user.get('username')} deactivated")
                                                    st.rerun()
                                                else:
                                                    st.error("Failed to deactivate user")
                                            except Exception as e:
                                                st.error(f"Error: {str(e)}")
                
                else:
                    st.info("No users found")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        with tab2:
            # Access Control Tab
            st.markdown('''
                <div class="content-card">
                    <h2>🔐 Access Control</h2>
                    <p>Configure access permissions and security settings.</p>
                    <br>
                    <p style="color: #9ca3af;">Coming soon: Permission matrix, role assignments, access logs...</p>
                </div>
            ''', unsafe_allow_html=True)
        
        with tab3:
            # User Activity Tab
            st.markdown('''
                <div class="content-card">
                    <h2>📊 User Activity</h2>
                    <p>Monitor user activities and system usage.</p>
                    <br>
                    <p style="color: #9ca3af;">Coming soon: Activity logs, login history, usage statistics...</p>
                </div>
            ''', unsafe_allow_html=True)
    
    def _render_new_assignment(self):
        """Render New Assignment section"""
        st.markdown('''
            <div class="content-card">
                <h2>➕ New Assignment</h2>
                <p>This section will allow you to create new assignments.</p>
                <br>
                <p style="color: #9ca3af;">Coming soon: Assignment creation form...</p>
            </div>
        ''', unsafe_allow_html=True)
    
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
        st.markdown('''
            <div class="app-header">
                <h1>⚙️ Admin Panel</h1>
            </div>
        ''', unsafe_allow_html=True)
        
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
