"""
User Management Tab for Admin Panel
Handles user CRUD operations and role assignments
"""

import streamlit as st
from auth_login.database import AuthenticationManager


class UserManagementTab:
    """User Management Tab - Manage users, roles, and permissions"""
    
    def __init__(self, auth_manager: AuthenticationManager):
        """
        Initialize User Management tab
        
        Args:
            auth_manager: AuthenticationManager instance for database operations
        """
        self.auth = auth_manager
    
    def render(self):
        """Render the User Management tab"""
        st.markdown("## 👥 User Management")
        
        # Add User Form
        self._render_add_user_form()
        
        st.markdown("---")
        
        # Display existing users
        st.markdown("### Existing Users")
        self._render_existing_users()
    
    def _render_add_user_form(self):
        """Render the add new user form"""
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
                        available_roles = self.auth.get_all_roles()
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
                            new_user = self.auth.create_user(
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
                                        self.auth.assign_role_to_user(
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
    
    def _render_existing_users(self):
        """Render existing users grouped by roles"""
        try:
            users = self.auth.get_all_users()
            all_roles = self.auth.get_all_roles()
            
            if users:
                # Create a mapping of role_id -> list of users
                users_by_role = {}
                users_without_roles = []
                
                # Get roles for each user and organize them
                for user in users:
                    user_roles = self.auth.get_user_roles(user['id'])
                    
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
                            # Create two columns: role heading on left, Manage Users button on right
                            col_role_title, col_manage_btn = st.columns([3, 1])
                            
                            with col_role_title:
                                st.markdown(f"#### 🧩 {role_name}")
                            
                            with col_manage_btn:
                                manage_btn_key = f"manage_Users_{role['id']}"
                                if st.button("Manage Users", key=manage_btn_key, type="secondary"):
                                    self._render_manage_Users_drawer(role['id'], role_name)
                            
                            # Add spacing between Manage Users button and user cards
                            # st.markdown("<br>", unsafe_allow_html=True)
                            
                            for user in users_by_role[role_name]:
                                self._render_user_card(user, suffix="role")
                            
                            st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Display roles without users
                    roles_without_users = [role for role in all_roles if role['name'] not in users_by_role]
                    
                    if roles_without_users:
                        st.markdown("#### 🛠 Roles Without Users")
                        # st.markdown("<br>", unsafe_allow_html=True)
                        
                        for role in roles_without_users:
                            # Create two columns: role heading on left, Manage Users button on right
                            col_role_title, col_manage_btn = st.columns([3, 1])
                            
                            with col_role_title:
                                st.markdown(f"<p style='font-size: 1.2rem; margin: 0;'>🧩 {role['name']}</p>", unsafe_allow_html=True)
                                st.markdown("_No users assigned_")
                            
                            with col_manage_btn:
                                manage_btn_key = f"manage_Users_empty_{role['id']}"
                                if st.button("Manage Users", key=manage_btn_key, type="secondary"):
                                    self._render_manage_Users_drawer(role['id'], role['name'])
                            
                            st.markdown("<br>", unsafe_allow_html=True)
                
                # Display users without roles
                if users_without_roles:
                    # Wrap in same column structure as Add New User form
                    col_norole_left, col_norole_center, col_norole_right = st.columns([0.01, 0.98, 0.01])
                    
                    with col_norole_center:
                        st.markdown("#### 👥 No Role Assigned")
                        
                        for user in users_without_roles:
                            self._render_user_card(user, suffix="norole")
            
            else:
                st.info("No users found")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    def _render_user_card(self, user, suffix=""):
        """
        Render a user card with details and actions
        
        Args:
            user: User dictionary
            suffix: Suffix for unique keys (e.g., "role" or "norole")
        """
        user_roles = self.auth.get_user_roles(user['id'])
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
                edit_key = f"edit_mode_{user.get('id')}_{suffix}"
                if edit_key not in st.session_state:
                    st.session_state[edit_key] = False
                
                if st.button("✏️ Edit", key=f"edit_btn_{user.get('id')}_{suffix}"):
                    st.session_state[edit_key] = not st.session_state[edit_key]
                    # Close the Manage Users drawer if it's open
                    st.session_state['manage_Users_drawer_open'] = False
                    st.rerun()
                
                if st.button("🗑️ Deactivate", key=f"deactivate_{user.get('id')}_{suffix}"):
                    try:
                        if self.auth.deactivate_user(user.get('id')):
                            st.success(f"User {user.get('username')} deactivated")
                            st.rerun()
                        else:
                            st.error("Failed to deactivate user")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            
            # Edit form in expander (shown when edit mode is active)
            if st.session_state.get(edit_key, False):
                self._render_edit_form(user, suffix)
    
    def _render_edit_form(self, user, suffix=""):
        """
        Render edit form for a user
        
        Args:
            user: User dictionary
            suffix: Suffix for unique keys
        """
        st.markdown("---")
        st.markdown(f"### ✏️ Edit User: {user.get('username')}")
        
        edit_key = f"edit_mode_{user.get('id')}_{suffix}"
        
        with st.form(f"edit_user_form_{user.get('id')}_{suffix}"):
            # Two columns for form fields
            col_edit1, col_edit2 = st.columns(2)
            
            with col_edit1:
                edit_username = st.text_input(
                    "Username *", 
                    value=user.get('username', ''),
                    key=f"edit_username_{user.get('id')}_{suffix}"
                )
                edit_full_name = st.text_input(
                    "Full Name", 
                    value=user.get('full_name', '') or '',
                    key=f"edit_fullname_{user.get('id')}_{suffix}"
                )
                edit_email = st.text_input(
                    "Email", 
                    value=user.get('email', '') or '',
                    key=f"edit_email_{user.get('id')}_{suffix}"
                )
            
            with col_edit2:
                edit_phone = st.text_input(
                    "Phone Number", 
                    value=user.get('phone_number', '') or '',
                    key=f"edit_phone_{user.get('id')}_{suffix}"
                )
                edit_new_password = st.text_input(
                    "New Password (leave blank to keep current)", 
                    type="password",
                    placeholder="Enter new password",
                    key=f"edit_password_{user.get('id')}_{suffix}"
                )
            
            # Checkboxes
            col_check1, col_check2 = st.columns(2)
            with col_check1:
                edit_admin = st.checkbox(
                    "Admin Rights", 
                    value=user.get('is_admin', False),
                    key=f"edit_admin_{user.get('id')}_{suffix}"
                )
            with col_check2:
                edit_active = st.checkbox(
                    "Active", 
                    value=user.get('is_active', True),
                    key=f"edit_active_{user.get('id')}_{suffix}"
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
                    updated_user = self.auth.update_user(
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
                        self.auth.update_user_password(
                            user.get('id'), 
                            edit_new_password
                        )
                    
                    if updated_user:
                        st.success(f"✅ User '{edit_username}' updated successfully!")
                        st.session_state[edit_key] = False
                        # Keep the Manage Users drawer closed
                        st.session_state['manage_Users_drawer_open'] = False
                        st.rerun()
                    else:
                        st.error("Failed to update user")
                except ValueError as e:
                    st.error(f"❌ {str(e)}")
                except Exception as e:
                    st.error(f"❌ Error updating user: {str(e)}")
        
        if cancel_submitted:
            st.session_state[edit_key] = False
            # Keep the Manage Users drawer closed
            st.session_state['manage_Users_drawer_open'] = False
            st.rerun()
    
    
    @st.dialog("Manage Users", width="medium")
    def _render_manage_Users_drawer(self, role_id, role_name):
        """
        Render the Manage Users modal dialog
        
        Args:
            role_id: The ID of the role to manage users for
            role_name: The name of the role
        """
        
        # Header with subtle blue accent - works in both light and dark
        st.markdown(f"""
            <div style='background: rgba(59, 130, 246, 0.08); padding: 12px 16px; 
                        margin: -1rem -1rem 1rem -1rem; border-radius: 8px 8px 0 0; 
                        border-left: 4px solid rgba(59, 130, 246, 0.5);'>
                <h3 style='margin: 0;'>Managing: <strong>{role_name}</strong></h3>
                <p style='margin: 4px 0 0 0; font-size: 0.9rem; opacity: 0.8;'>Add or remove users assigned to this role</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Current Users Section with blue accent border
        st.markdown("""
            <h4 style='margin-bottom: 12px; border-left: 3px solid rgba(59, 130, 246, 0.6); 
                       padding-left: 12px; margin-left: -8px;'>Current Users</h4>
        """, unsafe_allow_html=True)
        
        try:
            current_Users = self.auth.get_users_by_role(role_id)
            
            if current_Users:
                # Initialize session state for Users to remove
                if 'Users_to_remove' not in st.session_state:
                    st.session_state['Users_to_remove'] = set()
                
                for member in current_Users:
                    # Skip if marked for removal
                    if member['id'] in st.session_state['Users_to_remove']:
                        continue
                    
                    status_icon = "🟢" if member.get('is_active') else "🔴"
                    status_text = "Active" if member.get('is_active') else "Inactive"
                    
                    # Create member item with columns
                    col_member, col_status, col_remove = st.columns([3, 1, 1])
                    
                    with col_member:
                        st.markdown(f"<p style='font-size: 1.05rem; margin: 0; font-weight: 600;'>{member['username']}</p>", unsafe_allow_html=True)
                    
                    with col_status:
                        # Keep default text color, just adjust size and weight
                        st.markdown(f"<p style='font-size: 0.95rem; margin: 0; opacity: 0.9;'>{status_icon} {status_text}</p>", unsafe_allow_html=True)
                    
                    with col_remove:
                        if st.button("Remove", key=f"remove_{member['id']}", type="secondary", use_container_width=True):
                            st.session_state['Users_to_remove'].add(member['id'])
                            st.rerun()
            else:
                st.info("No Users currently assigned to this role")
        
        except Exception as e:
            st.error(f"Error loading current Users: {str(e)}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Add Users Section with blue accent border
        st.markdown("""
            <h4 style='margin-bottom: 12px; border-left: 3px solid rgba(59, 130, 246, 0.6); 
                       padding-left: 12px; margin-left: -8px;'>Add Users</h4>
        """, unsafe_allow_html=True)
        
        try:
            available_users = self.auth.get_users_not_in_role(role_id)
            
            # Add removed users back to available list (they haven't been saved yet)
            if 'Users_to_remove' in st.session_state:
                removed_users = self.auth.get_users_by_role(role_id)
                for user in removed_users:
                    if user['id'] in st.session_state['Users_to_remove']:
                        available_users.append(user)
            
            if available_users:
                # Initialize session state for Users to add
                if 'Users_to_add' not in st.session_state:
                    st.session_state['Users_to_add'] = set()
                
                user_options = {user['username']: user['id'] for user in available_users}
                
                selected_users = st.multiselect(
                    "Select users to add to this role",
                    options=list(user_options.keys()),
                    key="add_Users_dropdown",
                    placeholder="Choose users...",
                    label_visibility="collapsed"
                )
                
                if selected_users:
                    col_add1, col_add2 = st.columns([3, 1])
                    with col_add2:
                        if st.button("Add Selected", key="add_Users_btn", type="primary", use_container_width=True):
                            for username in selected_users:
                                st.session_state['Users_to_add'].add(user_options[username])
                            st.rerun()
                
                # Show users that will be added (pending save)
                if st.session_state.get('Users_to_add'):
                    st.success("**Users to be added (pending save):**")
                    for user in available_users:
                        if user['id'] in st.session_state['Users_to_add']:
                            st.markdown(f"<p style='font-size: 1.05rem; margin: 4px 0;'>- ✅ {user['username']}</p>", unsafe_allow_html=True)
            else:
                st.info("All active users are already assigned to this role")
        
        except Exception as e:
            st.error(f"Error loading available users: {str(e)}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Footer with Save/Cancel buttons
        col_footer1, col_footer2, col_footer3 = st.columns([2, 1, 1])
        
        with col_footer2:
            if st.button("Cancel", key="cancel_drawer", use_container_width=True):
                # Clear session state
                st.session_state['manage_Users_drawer_open'] = False
                st.session_state.pop('Users_to_add', None)
                st.session_state.pop('Users_to_remove', None)
                st.session_state.pop('manage_Users_role_id', None)
                st.session_state.pop('manage_Users_role_name', None)
                st.rerun()
        
        with col_footer3:
            if st.button("Save Changes", key="save_drawer", type="primary", use_container_width=True):
                try:
                    current_user_id = st.session_state.get('user_id')
                    changes_made = False
                    
                    # Remove users
                    if st.session_state.get('Users_to_remove'):
                        for user_id in st.session_state['Users_to_remove']:
                            if self.auth.remove_user_role(user_id, role_id):
                                changes_made = True
                    
                    # Add users
                    if st.session_state.get('Users_to_add'):
                        for user_id in st.session_state['Users_to_add']:
                            if self.auth.assign_role_to_user(user_id, role_id, current_user_id):
                                changes_made = True
                    
                    if changes_made:
                        st.success(f"✅ Successfully updated Users for '{role_name}'!")
                    
                    # Clear session state
                    st.session_state['manage_Users_drawer_open'] = False
                    st.session_state.pop('Users_to_add', None)
                    st.session_state.pop('Users_to_remove', None)
                    st.session_state.pop('manage_Users_role_id', None)
                    st.session_state.pop('manage_Users_role_name', None)
                    st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Error saving changes: {str(e)}")




