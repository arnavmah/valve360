import streamlit as st
import sys
import os
import time
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
                                            # Initialize session state for edit mode
                                            edit_key = f"edit_mode_{user.get('id')}_role"
                                            if edit_key not in st.session_state:
                                                st.session_state[edit_key] = False
                                            
                                            if st.button("✏️ Edit", key=f"edit_btn_{user.get('id')}_role"):
                                                st.session_state[edit_key] = not st.session_state[edit_key]
                                                st.rerun()
                                            
                                            if st.button("🗑️ Deactivate", key=f"deactivate_{user.get('id')}_role"):
                                                try:
                                                    if self.admin_manager.auth.deactivate_user(user.get('id')):
                                                        st.success(f"User {user.get('username')} deactivated")
                                                        st.rerun()
                                                    else:
                                                        st.error("Failed to deactivate user")
                                                except Exception as e:
                                                    st.error(f"Error: {str(e)}")
                                        
                                        # Edit form in expander (shown when edit mode is active)
                                        if st.session_state.get(edit_key, False):
                                            st.markdown("---")
                                            st.markdown(f"### ✏️ Edit User: {user.get('username')}")
                                            
                                            with st.form(f"edit_user_form_{user.get('id')}_role"):
                                                # Two columns for form fields
                                                col_edit1, col_edit2 = st.columns(2)
                                                
                                                with col_edit1:
                                                    edit_username = st.text_input(
                                                        "Username *", 
                                                        value=user.get('username', ''),
                                                        key=f"edit_username_{user.get('id')}_role"
                                                    )
                                                    edit_full_name = st.text_input(
                                                        "Full Name", 
                                                        value=user.get('full_name', '') or '',
                                                        key=f"edit_fullname_{user.get('id')}_role"
                                                    )
                                                    edit_email = st.text_input(
                                                        "Email", 
                                                        value=user.get('email', '') or '',
                                                        key=f"edit_email_{user.get('id')}_role"
                                                    )
                                                
                                                with col_edit2:
                                                    edit_phone = st.text_input(
                                                        "Phone Number", 
                                                        value=user.get('phone_number', '') or '',
                                                        key=f"edit_phone_{user.get('id')}_role"
                                                    )
                                                    edit_new_password = st.text_input(
                                                        "New Password (leave blank to keep current)", 
                                                        type="password",
                                                        placeholder="Enter new password",
                                                        key=f"edit_password_{user.get('id')}_role"
                                                    )
                                                
                                                # Checkboxes
                                                col_check1, col_check2 = st.columns(2)
                                                with col_check1:
                                                    edit_admin = st.checkbox(
                                                        "Admin Rights", 
                                                        value=user.get('is_admin', False),
                                                        key=f"edit_admin_{user.get('id')}_role"
                                                    )
                                                with col_check2:
                                                    edit_active = st.checkbox(
                                                        "Active", 
                                                        value=user.get('is_active', True),
                                                        key=f"edit_active_{user.get('id')}_role"
                                                    )
                                                
                                                # Submit and Cancel buttons
                                                col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
                                                with col_btn1:
                                                    save_submitted = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
                                                with col_btn2:
                                                    cancel_submitted = st.form_submit_button("❌ Cancel", use_container_width=True)
                                            
                                            if save_submitted:
                                                if not edit_username:
                                                    st.error("Username is required!")
                                                else:
                                                    try:
                                                        # Update user information
                                                        updated_user = self.admin_manager.auth.update_user(
                                                            user_id=user.get('id'),
                                                            username=edit_username,
                                                            email=edit_email if edit_email else None,
                                                            full_name=edit_full_name if edit_full_name else None,
                                                            phone_number=edit_phone if edit_phone else None,
                                                            is_admin=edit_admin,
                                                            is_active=edit_active
                                                        )
                                                        
                                                        # Update password if provided
                                                        if edit_new_password:
                                                            self.admin_manager.auth.update_user_password(
                                                                user.get('id'), 
                                                                edit_new_password
                                                            )
                                                        
                                                        if updated_user:
                                                            st.success(f"✅ User '{edit_username}' updated successfully!")
                                                            st.session_state[edit_key] = False
                                                            st.rerun()
                                                        else:
                                                            st.error("Failed to update user")
                                                    except ValueError as e:
                                                        st.error(f"❌ {str(e)}")
                                                    except Exception as e:
                                                        st.error(f"❌ Error updating user: {str(e)}")
                                            
                                            if cancel_submitted:
                                                st.session_state[edit_key] = False
                                                st.rerun()
                                
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
                                        # Initialize session state for edit mode
                                        edit_key = f"edit_mode_{user.get('id')}_norole"
                                        if edit_key not in st.session_state:
                                            st.session_state[edit_key] = False
                                        
                                        if st.button("✏️ Edit", key=f"edit_btn_{user.get('id')}_norole"):
                                            st.session_state[edit_key] = not st.session_state[edit_key]
                                            st.rerun()
                                        
                                        if st.button("🗑️ Deactivate", key=f"deactivate_{user.get('id')}_norole"):
                                            try:
                                                if self.admin_manager.auth.deactivate_user(user.get('id')):
                                                    st.success(f"User {user.get('username')} deactivated")
                                                    st.rerun()
                                                else:
                                                    st.error("Failed to deactivate user")
                                            except Exception as e:
                                                st.error(f"Error: {str(e)}")
                                    
                                    # Edit form in expander (shown when edit mode is active)
                                    if st.session_state.get(edit_key, False):
                                        st.markdown("---")
                                        st.markdown(f"### ✏️ Edit User: {user.get('username')}")
                                        
                                        with st.form(f"edit_user_form_{user.get('id')}_norole"):
                                            # Two columns for form fields
                                            col_edit1, col_edit2 = st.columns(2)
                                            
                                            with col_edit1:
                                                edit_username = st.text_input(
                                                    "Username *", 
                                                    value=user.get('username', ''),
                                                    key=f"edit_username_{user.get('id')}_norole"
                                                )
                                                edit_full_name = st.text_input(
                                                    "Full Name", 
                                                    value=user.get('full_name', '') or '',
                                                    key=f"edit_fullname_{user.get('id')}_norole"
                                                )
                                                edit_email = st.text_input(
                                                    "Email", 
                                                    value=user.get('email', '') or '',
                                                    key=f"edit_email_{user.get('id')}_norole"
                                                )
                                            
                                            with col_edit2:
                                                edit_phone = st.text_input(
                                                    "Phone Number", 
                                                    value=user.get('phone_number', '') or '',
                                                    key=f"edit_phone_{user.get('id')}_norole"
                                                )
                                                edit_new_password = st.text_input(
                                                    "New Password (leave blank to keep current)", 
                                                    type="password",
                                                    placeholder="Enter new password",
                                                    key=f"edit_password_{user.get('id')}_norole"
                                                )
                                            
                                            # Checkboxes
                                            col_check1, col_check2 = st.columns(2)
                                            with col_check1:
                                                edit_admin = st.checkbox(
                                                    "Admin Rights", 
                                                    value=user.get('is_admin', False),
                                                    key=f"edit_admin_{user.get('id')}_norole"
                                                )
                                            with col_check2:
                                                edit_active = st.checkbox(
                                                    "Active", 
                                                    value=user.get('is_active', True),
                                                    key=f"edit_active_{user.get('id')}_norole"
                                                )
                                            
                                            # Submit and Cancel buttons
                                            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
                                            with col_btn1:
                                                save_submitted = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
                                            with col_btn2:
                                                cancel_submitted = st.form_submit_button("❌ Cancel", use_container_width=True)
                                        
                                        if save_submitted:
                                            if not edit_username:
                                                st.error("Username is required!")
                                            else:
                                                try:
                                                    # Update user information
                                                    updated_user = self.admin_manager.auth.update_user(
                                                        user_id=user.get('id'),
                                                        username=edit_username,
                                                        email=edit_email if edit_email else None,
                                                        full_name=edit_full_name if edit_full_name else None,
                                                        phone_number=edit_phone if edit_phone else None,
                                                        is_admin=edit_admin,
                                                        is_active=edit_active
                                                    )
                                                    
                                                    # Update password if provided
                                                    if edit_new_password:
                                                        self.admin_manager.auth.update_user_password(
                                                            user.get('id'), 
                                                            edit_new_password
                                                        )
                                                    
                                                    if updated_user:
                                                        st.success(f"✅ User '{edit_username}' updated successfully!")
                                                        st.session_state[edit_key] = False
                                                        st.rerun()
                                                    else:
                                                        st.error("Failed to update user")
                                                except ValueError as e:
                                                    st.error(f"❌ {str(e)}")
                                                except Exception as e:
                                                    st.error(f"❌ Error updating user: {str(e)}")
                                        
                                        if cancel_submitted:
                                            st.session_state[edit_key] = False
                                            st.rerun()
                
                else:
                    st.info("No users found")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        with tab2:
            # Access Control Tab
            st.markdown("## 🔐 Access Control")
            st.markdown("Manage user roles, permissions, and access rules for the system.")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Create sub-tabs for Access Control
            access_tab1, access_tab2, access_tab3 = st.tabs([
                "🔑 Permissions", 
                "👥 Roles", 
                "🔗 Role-Permission Assignment"
            ])
            
            with access_tab1:
                # Permissions Management
                st.markdown("### Permission Management")
                
                # Limit form width
                col_perm_left, col_perm_center, col_perm_right = st.columns([0.01, 0.98, 0.01])
                
                with col_perm_center:
                    with st.expander("➕ Add New Permission", expanded=False):
                        with st.form("add_permission_form", clear_on_submit=True):
                            # Two columns for form fields
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                perm_name = st.text_input(
                                    "Permission Name *", 
                                    placeholder="e.g., view_reports",
                                    key="new_perm_name"
                                )
                                perm_module = st.text_input(
                                    "Module", 
                                    placeholder="e.g., reports",
                                    key="new_perm_module"
                                )
                            
                            with col2:
                                perm_action = st.text_input(
                                    "Action", 
                                    placeholder="e.g., view, create, edit, delete",
                                    key="new_perm_action"
                                )
                                perm_description = st.text_area(
                                    "Description", 
                                    placeholder="Describe what this permission allows",
                                    key="new_perm_description",
                                    height=100
                                )
                            
                            # Submit button
                            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
                            with col_btn2:
                                perm_submitted = st.form_submit_button(
                                    "Create Permission", 
                                    type="primary", 
                                    use_container_width=True
                                )
                        
                        if perm_submitted:
                            if not perm_name:
                                st.error("Permission name is required!")
                            else:
                                try:
                                    new_perm = self.admin_manager.auth.create_permission(
                                        name=perm_name,
                                        description=perm_description if perm_description else None,
                                        module=perm_module if perm_module else None,
                                        action=perm_action if perm_action else None
                                    )
                                    if new_perm:
                                        st.success(f"✅ Permission '{perm_name}' created successfully!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to create permission")
                                except ValueError as e:
                                    st.error(f"❌ {str(e)}")
                                except Exception as e:
                                    st.error(f"❌ Error creating permission: {str(e)}")
                
                st.markdown("---")
                
                # Display permissions as a matrix
                st.markdown("### Permission Matrix")
                
                # Wrap in same column structure as Add New Permission
                col_matrix_left, col_matrix_center, col_matrix_right = st.columns([0.01, 0.98, 0.01])
                
                with col_matrix_center:
                    try:
                        permissions = self.admin_manager.auth.get_all_permissions()
                        
                        if permissions:
                            # Build matrix structure
                            # Get unique modules and actions
                            modules = sorted(list(set([p.get('module', 'General') for p in permissions])))
                            actions = sorted(list(set([p.get('action', 'N/A') for p in permissions])))
                            
                            # Create permission lookup
                            perm_lookup = {}
                            for perm in permissions:
                                module = perm.get('module', 'General')
                                action = perm.get('action', 'N/A')
                                key = f"{module}_{action}"
                                perm_lookup[key] = perm
                            
                            # Create matrix HTML with proper styling
                            matrix_html = """
                            <style>
                            .permission-matrix-wrapper {
                                max-height: 400px;
                                overflow-y: auto;
                                border-radius: 12px;
                                margin: 20px 0;
                                position: relative;
                            }
                            .permission-matrix {
                                width: 100%;
                                border-collapse: collapse;
                                background: rgba(26, 26, 46, 0.6);
                            }
                            .permission-matrix thead tr {
                                position: sticky;
                                top: 0;
                                z-index: 10;
                            }
                            .permission-matrix th {
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                color: white;
                                padding: 15px;
                                text-align: center;
                                font-weight: 600;
                                font-size: 1em;
                                border: 1px solid rgba(255, 255, 255, 0.1);
                                position: sticky;
                                top: 0;
                            }
                            .permission-matrix td {
                                padding: 12px;
                                text-align: center;
                                border: 1px solid rgba(255, 255, 255, 0.1);
                                color: #fff;
                                background: rgba(26, 26, 46, 0.6);
                            }
                            .permission-matrix tbody tr:hover td {
                                background: rgba(102, 126, 234, 0.2);
                            }
                            .permission-matrix .module-cell {
                                text-align: left;
                                font-weight: 600;
                                color: #e0e0e0;
                                padding-left: 20px;
                            }
                            .check-icon {
                                color: #10b981;
                                font-size: 1.5em;
                            }
                            .cross-icon {
                                color: #ef4444;
                                font-size: 1.2em;
                                opacity: 0.3;
                            }
                            </style>
                            <div class="permission-matrix-wrapper">
                            <table class="permission-matrix">
                                <thead>
                                    <tr>
                                        <th>Module</th>
"""
                            
                            # Add action headers
                            for action in actions:
                                matrix_html += f"                                    <th>{action.capitalize()}</th>\n"
                            
                            matrix_html += """                                </tr>
                                </thead>
                                <tbody>
"""
                            
                            # Add rows for each module
                            for module in modules:
                                matrix_html += f"""                                <tr>
                                        <td class="module-cell">📦 {module}</td>
"""
                                
                                for action in actions:
                                    key = f"{module}_{action}"
                                    if key in perm_lookup:
                                        # Permission exists - show checkmark
                                        matrix_html += '                                    <td><span class="check-icon">✓</span></td>\n'
                                    else:
                                        # Permission doesn't exist - show cross
                                        matrix_html += '                                    <td><span class="cross-icon">✕</span></td>\n'
                                
                                matrix_html += "                                </tr>\n"
                            
                            matrix_html += """                            </tbody>
                            </table>
                            </div>
"""
                            
                            # Render the HTML table using markdown with unsafe_allow_html
                            st.markdown(matrix_html, unsafe_allow_html=True)
                            
                            # Show total count
                            st.info(f"📊 Total Permissions: {len(permissions)} | Modules: {len(modules)} | Actions: {len(actions)}")
                            
                        else:
                            st.info("No permissions found in the database")
                    except Exception as e:
                        st.error(f"Error loading permissions: {str(e)}")
            
            
            with access_tab2:
                # Roles Management
                st.markdown("### Role Management")
                
                # Wrap in same column structure
                col_role_left, col_role_center, col_role_right = st.columns([0.01, 0.98, 0.01])
                
                with col_role_center:
                    with st.expander("➕ Add New Role", expanded=False):
                        with st.form("add_role_form", clear_on_submit=True):
                            # Form fields
                            role_name = st.text_input(
                                "Role Name *", 
                                placeholder="e.g., System Administrator",
                                key="new_role_name"
                            )
                            role_description = st.text_area(
                                "Description", 
                                placeholder="Describe the role's purpose and responsibilities",
                                key="new_role_description",
                                height=100
                            )
                            
                            # Submit button
                            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
                            with col_btn2:
                                role_submitted = st.form_submit_button(
                                    "Create Role", 
                                    type="primary", 
                                    use_container_width=True
                                )
                        
                        if role_submitted:
                            if not role_name:
                                st.error("Role name is required!")
                            else:
                                try:
                                    # Get current user ID from session state
                                    created_by = st.session_state.get('user_id', None)
                                    new_role = self.admin_manager.auth.create_role(
                                        name=role_name,
                                        description=role_description if role_description else None,
                                        created_by=created_by
                                    )
                                    if new_role:
                                        st.success(f"✅ Role '{role_name}' created successfully!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to create role")
                                except ValueError as e:
                                    st.error(f"❌ {str(e)}")
                                except Exception as e:
                                    st.error(f"❌ Error creating role: {str(e)}")
                
                st.markdown("---")
                
                # Display existing roles
                st.markdown("### Existing Roles")
                
                col_roles_left, col_roles_center, col_roles_right = st.columns([0.01, 0.98, 0.01])
                
                with col_roles_center:
                    try:
                        roles = self.admin_manager.auth.get_all_roles()
                        
                        if roles:
                            for role in roles:
                                # Get permissions for this role
                                role_permissions = self.admin_manager.auth.get_role_permissions(role['id'])
                                
                                # Create expander for each role
                                with st.expander(f"🔷 {role.get('name')} (System Role)", expanded=False):
                                    st.markdown(f"**Description:** {role.get('description', 'N/A')}")
                                    st.markdown(f"**Created:** {role.get('created_by', 'N/A')}")
                                    st.markdown(f"**Assigned Permissions:** {len(role_permissions)}")
                                    
                                    # View Assigned Permissions in nested expander
                                    if role_permissions:
                                        with st.expander("View Assigned Permissions", expanded=False):
                                            st.markdown("**Permissions by Module**")
                                            
                                            # Group permissions by module
                                            perms_by_module = {}
                                            for perm in role_permissions:
                                                module = perm.get('module', 'General')
                                                if module not in perms_by_module:
                                                    perms_by_module[module] = []
                                                perms_by_module[module].append(perm)
                                            
                                            # Display permissions grouped by module (compact format)
                                            for module, perms in perms_by_module.items():
                                                # Get all actions for this module
                                                actions = [perm.get('action', 'N/A').capitalize() for perm in perms]
                                                # Display module with all actions on one line
                                                st.markdown(f"📦 **{module.capitalize()}** --> {', '.join(actions)}")
                                    else:
                                        st.info("No permissions assigned to this role")
                        else:
                            st.info("No roles found")
                    except Exception as e:
                        st.error(f"Error loading roles: {str(e)}")
            
            with access_tab3:
                # Role-Permission Assignment
                st.markdown("### Role-Permission Assignment")
                st.markdown("Coming soon: Assign permissions to roles")
        
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
