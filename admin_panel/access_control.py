"""
Access Control Tab for Admin Panel
Handles permissions, roles, and role-permission assignments
"""

import streamlit as st
from auth_login.database import AuthenticationManager


class AccessControlTab:
    """Access Control Tab - Manage roles, permissions, and access rules"""
    
    def __init__(self, auth_manager: AuthenticationManager):
        """
        Initialize Access Control tab
        
        Args:
            auth_manager: AuthenticationManager instance for database operations
        """
        self.auth = auth_manager
    
    def render(self):
        """Render the Access Control tab"""
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
            self._render_permissions_tab()
        
        with access_tab2:
            self._render_roles_tab()
        
        with access_tab3:
            self._render_role_permission_assignment_tab()
    
    def _render_permissions_tab(self):
        """Render the Permissions Management tab"""
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
                            new_perm = self.auth.create_permission(
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
                permissions = self.auth.get_all_permissions()
                
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
                    
                    # Create permission matrix data structure
                    matrix_data = []
                    
                    for module in modules:
                        row = {"Module": f"📦 {module}"}
                        for action in actions:
                            key = f"{module}_{action}"
                            row[action.capitalize()] = "✓" if key in perm_lookup else "✕"
                        matrix_data.append(row)
                    
                    # Display using standard Streamlit dataframe
                    st.dataframe(
                        matrix_data, 
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Show total count
                    st.info(f"📊 Total Permissions: {len(permissions)} | Modules: {len(modules)} | Actions: {len(actions)}")
                    
                else:
                    st.info("No permissions found in the database")
            except Exception as e:
                st.error(f"Error loading permissions: {str(e)}")
    
    def _render_roles_tab(self):
        """Render the Roles Management tab"""
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
                            new_role = self.auth.create_role(
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
                roles = self.auth.get_all_roles()
                
                if roles:
                    for role in roles:
                        # Get permissions for this role
                        role_permissions = self.auth.get_role_permissions(role['id'])
                        
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
    
    def _render_role_permission_assignment_tab(self):
        """Render the Role-Permission Assignment tab"""
        st.markdown("### Role-Permission Assignment")
        st.markdown("Coming soon: Assign permissions to roles")
