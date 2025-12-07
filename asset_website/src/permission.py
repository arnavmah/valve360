import sys
import os
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'auth_login'))

from database import AuthenticationManager

class PermissionManager:
    """Permission manager for role-based access control"""
    
    def __init__(self):
        """Initialize permission manager with database connection"""
        self.auth_manager = AuthenticationManager()
    
    # ==================== PERMISSION CHECKS ====================
    
    def check_permission(self, user_id: int, permission_name: str) -> bool:
        """Check if user has a specific permission"""
        return self.auth_manager.has_permission(user_id, permission_name)
    
    def check_permissions(self, user_id: int, permissions: List[str]) -> bool:
        """Check if user has ALL permissions in the list"""
        for permission in permissions:
            if not self.check_permission(user_id, permission):
                return False
        return True
    
    def check_any_permission(self, user_id: int, permissions: List[str]) -> bool:
        """Check if user has ANY permission in the list"""
        for permission in permissions:
            if self.check_permission(user_id, permission):
                return True
        return False
    
    # ==================== USER PERMISSIONS ====================
    
    def get_user_permissions(self, user_id: int) -> List[Dict]:
        """Get all permissions for a user"""
        return self.auth_manager.get_user_permissions(user_id)
    
    def get_permission_names(self, user_id: int) -> List[str]:
        """Get list of permission names for a user"""
        permissions = self.get_user_permissions(user_id)
        return [p['name'] for p in permissions]
    
    # ==================== USER ROLES ====================
    
    def get_user_roles(self, user_id: int) -> List[Dict]:
        """Get all roles assigned to a user"""
        return self.auth_manager.get_user_roles(user_id)
    
    def get_role_names(self, user_id: int) -> List[str]:
        """Get list of role names for a user"""
        roles = self.get_user_roles(user_id)
        return [r['name'] for r in roles]
    
    def assign_role(self, user_id: int, role_id: int, assigned_by: int = None) -> bool:
        """Assign a role to a user"""
        return self.auth_manager.assign_role_to_user(user_id, role_id, assigned_by)
    
    def remove_role(self, user_id: int, role_id: int) -> bool:
        """Remove a role from a user"""
        return self.auth_manager.remove_user_role(user_id, role_id)
    
    # ==================== ROLE LOOKUP ====================
    
    def get_role_by_name(self, role_name: str) -> Optional[Dict]:
        """Get role by name"""
        return self.auth_manager.get_role_by_name(role_name)
    
    def get_all_permissions(self) -> List[Dict]:
        """Get all available permissions in the system"""
        return self.auth_manager.get_all_permissions()
    
    # ==================== ADMIN CHECKS ====================
    
    def is_admin(self, user_id: int) -> bool:
        """Check if user is an admin"""
        user = self.auth_manager.get_user_by_id(user_id)
        if user is None:
            return False
        return user.get('is_admin', False)
    
    def is_active(self, user_id: int) -> bool:
        """Check if user is active"""
        user = self.auth_manager.get_user_by_id(user_id)
        if user is None:
            return False
        return user.get('is_active', False)
    
    def close(self):
        """Close database connection pool"""
        self.auth_manager.close_pool()


if __name__ == "__main__":
    # Test permission manager
    pm = PermissionManager()
    
    print("✅ PermissionManager module loaded successfully!")
    print("\n📋 Available methods:")
    print("   - check_permission(user_id, permission_name)")
    print("   - check_permissions(user_id, [permissions])")
    print("   - check_any_permission(user_id, [permissions])")
    print("   - get_user_permissions(user_id)")
    print("   - get_permission_names(user_id)")
    print("   - get_user_roles(user_id)")
    print("   - get_role_names(user_id)")
    print("   - is_admin(user_id)")
    print("   - is_active(user_id)")
    
    pm.close()
