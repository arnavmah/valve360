import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import bcrypt
import logging
from typing import Dict, List, Optional

# Load environment variables from .env file
load_dotenv()

# Configure logging with absolute path
log_dir = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
    filename=os.path.join(log_dir, 'auth_errors.log'),
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AuthenticationManager:
    """Authentication manager for user login with role-based access control"""
    
    def __init__(self, connection_string: str = None):
        """Initialize authentication manager with database connection"""
        self.connection_string = connection_string or os.getenv('DATABASE_URL')
        
        if not self.connection_string:
            raise ValueError("DATABASE_URL not found in environment variables")
        
        try:
            self.pool = SimpleConnectionPool(1, 10, self.connection_string)
        except Exception as e:
            logging.error(f"Failed to initialize connection pool: {e}")
            raise Exception("Failed to initialize connection pool")
    
    @contextmanager
    def get_connection(self):
        """Get a database connection from the pool"""
        conn = self.pool.getconn()
        try:
            yield conn
        finally:
            self.pool.putconn(conn)
    
    @contextmanager
    def get_cursor(self):
        """Get a cursor for executing queries"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            try:
                yield cursor
                conn.commit()
            except Exception as e:
                conn.rollback()
                logging.error(f"Database query error: {e}")
                raise
            finally:
                cursor.close()
    
    # ==================== PASSWORD SECURITY ====================
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt with salt"""
        try:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            logging.error(f"Error hashing password: {e}")
            raise
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'), 
                hashed_password.encode('utf-8')
            )
        except Exception as e:
            logging.error(f"Error verifying password: {e}")
            return False
    
    # ==================== USER AUTHENTICATION ====================
    
    def create_user(self, username: str, password: str, email: str = None, 
                   full_name: str = None, phone_number: str = None,
                   is_admin: bool = False, created_by: int = None, extra: str = None) -> Optional[Dict]:
        """Create a new user with hashed password"""
        if not username or not password:
            raise ValueError("Username and password are required")
        
        # Check if user already exists
        existing_user = self.get_user_by_username(username)
        if existing_user:
            raise ValueError(f"User '{username}' already exists")
        
        password_hash = self.hash_password(password)
        
        query = """
            INSERT INTO users (username, password_hash, email, full_name, phone_number, 
                              is_admin, is_active, created_by, extra)
            VALUES (%s, %s, %s, %s, %s, %s, TRUE, %s, %s)
            RETURNING id, username, email, full_name, phone_number, is_admin, is_active, last_login, created_by, extra
        """
        
        try:
            with self.get_cursor() as cur:
                cur.execute(query, (username, password_hash, email, full_name, 
                                   phone_number, is_admin, created_by, extra))
                result = cur.fetchone()
                return dict(result) if result else None
        except Exception as e:
            logging.error(f"Error creating user: {e}")
            raise
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        query = """
            SELECT id, username, password_hash, email, full_name, phone_number, 
                   is_admin, is_active, last_login, created_by, extra
            FROM users
            WHERE username = %s AND is_active = TRUE
        """
        
        try:
            with self.get_cursor() as cur:
                cur.execute(query, (username,))
                result = cur.fetchone()
                return dict(result) if result else None
        except Exception as e:
            logging.error(f"Error fetching user: {e}")
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """
        Authenticate user with username and password.
        Returns user data if successful, None if failed.
        """
        user = self.get_user_by_username(username)
        
        if not user:
            logging.warning(f"Login attempt for non-existent user: {username}")
            return None
        
        if not self.verify_password(password, user['password_hash']):
            logging.warning(f"Failed login attempt for user: {username}")
            return None
        
        # Update last login
        self.update_last_login(user['id'])
        
        # Remove password hash from response
        user_data = dict(user)
        del user_data['password_hash']
        
        logging.info(f"User {username} logged in successfully")
        return user_data
    
    def update_last_login(self, user_id: int) -> bool:
        """Update user's last login timestamp"""
        query = """
            UPDATE users
            SET last_login = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        
        try:
            with self.get_cursor() as cur:
                cur.execute(query, (user_id,))
                return cur.rowcount > 0
        except Exception as e:
            logging.error(f"Error updating last login: {e}")
            return False
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        query = """
            SELECT id, username, email, full_name, phone_number, 
                   is_admin, is_active, last_login, created_by, extra
            FROM users
            WHERE id = %s AND is_active = TRUE
        """
        
        try:
            with self.get_cursor() as cur:
                cur.execute(query, (user_id,))
                result = cur.fetchone()
                return dict(result) if result else None
        except Exception as e:
            logging.error(f"Error fetching user by ID: {e}")
            return None
    
    def update_user_password(self, user_id: int, new_password: str) -> bool:
        """Update user password"""
        if not new_password:
            raise ValueError("New password is required")
        
        password_hash = self.hash_password(new_password)
        
        query = """
            UPDATE users
            SET password_hash = %s
            WHERE id = %s
            RETURNING id
        """
        
        try:
            with self.get_cursor() as cur:
                cur.execute(query, (password_hash, user_id))
                return cur.fetchone() is not None
        except Exception as e:
            logging.error(f"Error updating password: {e}")
            return False
    
    # ==================== ROLE MANAGEMENT ====================
    
    def assign_role_to_user(self, user_id: int, role_id: int, assigned_by: int = None) -> bool:
        """Assign a role to a user"""
        query = """
            INSERT INTO user_roles (role_id, user_id, assigned_by)
            VALUES (%s, %s, %s)
            ON CONFLICT (role_id, user_id) DO NOTHING
            RETURNING id
        """
        
        try:
            with self.get_cursor() as cur:
                cur.execute(query, (role_id, user_id, assigned_by))
                return cur.fetchone() is not None
        except Exception as e:
            logging.error(f"Error assigning role to user: {e}")
            return False
    
    def get_user_roles(self, user_id: int) -> List[Dict]:
        """Get all roles assigned to a user"""
        query = """
            SELECT r.id, r.name, r.description, r.is_active
            FROM roles r
            JOIN user_roles ur ON r.id = ur.role_id
            WHERE ur.user_id = %s AND r.is_active = TRUE
        """
        
        try:
            with self.get_cursor() as cur:
                cur.execute(query, (user_id,))
                rows = cur.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"Error fetching user roles: {e}")
            return []
    

    def create_role(self, name: str, description: str = None, created_by: int = None) -> Optional[Dict]:
        """Create a new role"""
        if not name:
            raise ValueError("Role name is required")
        
        # Check if role already exists
        query_check = "SELECT id FROM roles WHERE name = %s"
        try:
            with self.get_cursor() as cur:
                cur.execute(query_check, (name,))
                if cur.fetchone():
                    raise ValueError(f"Role '{name}' already exists")
        except ValueError:
            raise
        except Exception as e:
            logging.error(f"Error checking role: {e}")
            raise
        
        query = """
            INSERT INTO roles (name, description, created_by, is_active)
            VALUES (%s, %s, %s, TRUE)
            RETURNING id, name, description, created_by, is_active
        """
        
        try:
            with self.get_cursor() as cur:
                cur.execute(query, (name, description, created_by))
                result = cur.fetchone()
                return dict(result) if result else None
        except Exception as e:
            logging.error(f"Error creating role: {e}")
            raise


    def get_all_roles(self) -> List[Dict]:
        """Get all active roles"""
        query = """
            SELECT id, name, description, is_active
            FROM roles
            WHERE is_active = TRUE
            ORDER BY name
        """
        
        try:
            with self.get_cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"Error fetching roles: {e}")
            return []
    
    def get_role_by_name(self, role_name: str) -> Optional[Dict]:
        """Get role by name"""
        query = """
            SELECT id, name, description, is_active
            FROM roles
            WHERE name = %s AND is_active = TRUE
        """
        
        try:
            with self.get_cursor() as cur:
                cur.execute(query, (role_name,))
                result = cur.fetchone()
                return dict(result) if result else None
        except Exception as e:
            logging.error(f"Error fetching role: {e}")
            return None
    
    # ==================== PERMISSIONS ====================
    
    def get_user_permissions(self, user_id: int) -> List[Dict]:
        """Get all permissions for a user through their roles"""
        query = """
            SELECT DISTINCT p.id, p.name, p.description, p.module, p.action
            FROM permissions p
            JOIN permission_roles pr ON p.id = pr.permission_id
            JOIN roles r ON pr.role_id = r.id
            JOIN user_roles ur ON r.id = ur.role_id
            WHERE ur.user_id = %s AND r.is_active = TRUE
        """
        
        try:
            with self.get_cursor() as cur:
                cur.execute(query, (user_id,))
                rows = cur.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"Error fetching user permissions: {e}")
            return []
    
    def has_permission(self, user_id: int, permission_name: str) -> bool:
        """Check if user has a specific permission"""
        # Admin users have all permissions
        user = self.get_user_by_id(user_id)
        if user and user['is_admin']:
            return True
        
        query = """
            SELECT EXISTS (
                SELECT 1 FROM permissions p
                JOIN permission_roles pr ON p.id = pr.permission_id
                JOIN roles r ON pr.role_id = r.id
                JOIN user_roles ur ON r.id = ur.role_id
                WHERE ur.user_id = %s AND p.name = %s AND r.is_active = TRUE
            )
        """
        
        try:
            with self.get_cursor() as cur:
                cur.execute(query, (user_id, permission_name))
                result = cur.fetchone()
                return result[0] if result else False
        except Exception as e:
            logging.error(f"Error checking permission: {e}")
            return False
    
    def get_all_permissions(self) -> List[Dict]:
        """Get all available permissions"""
        query = """
            SELECT id, name, description, module, action
            FROM permissions
            ORDER BY module, action
        """
        
        try:
            with self.get_cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"Error fetching permissions: {e}")
            return []
    
    def create_permission(self, name: str, description: str = None, 
                         module: str = None, action: str = None) -> Optional[Dict]:
        """Create a new permission"""
        if not name:
            raise ValueError("Permission name is required")
        
        # Check if permission already exists
        query_check = "SELECT id FROM permissions WHERE name = %s"
        try:
            with self.get_cursor() as cur:
                cur.execute(query_check, (name,))
                if cur.fetchone():
                    raise ValueError(f"Permission '{name}' already exists")
        except ValueError:
            raise
        except Exception as e:
            logging.error(f"Error checking permission: {e}")
            raise
        
        query = """
            INSERT INTO permissions (name, description, module, action)
            VALUES (%s, %s, %s, %s)
            RETURNING id, name, description, module, action
        """
        
        try:
            with self.get_cursor() as cur:
                cur.execute(query, (name, description, module, action))
                result = cur.fetchone()
                return dict(result) if result else None
        except Exception as e:
            logging.error(f"Error creating permission: {e}")
            raise
    

    
    def get_role_permissions(self, role_id: int) -> List[Dict]:
        """Get all permissions assigned to a role"""
        query = """
            SELECT p.id, p.name, p.description, p.module, p.action
            FROM permissions p
            INNER JOIN permission_roles pr ON p.id = pr.permission_id
            WHERE pr.role_id = %s
            ORDER BY p.module, p.action
        """
        
        try:
            with self.get_cursor() as cur:
                cur.execute(query, (role_id,))
                rows = cur.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"Error fetching role permissions: {e}")
            return []
    
    # ==================== USER MANAGEMENT ====================
    
    def get_all_users(self) -> List[Dict]:
        """Get all active users"""
        query = """
            SELECT id, username, email, full_name, phone_number, 
                   is_admin, is_active, last_login, created_by
            FROM users
            WHERE is_active = TRUE
            ORDER BY id DESC
        """
        
        try:
            with self.get_cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logging.error(f"Error fetching users: {e}")
            return []
    
    def update_user_admin_status(self, user_id: int, is_admin: bool) -> bool:
        """Update user admin status"""
        query = """
            UPDATE users
            SET is_admin = %s
            WHERE id = %s
            RETURNING id
        """
        
        try:
            with self.get_cursor() as cur:
                cur.execute(query, (is_admin, user_id))
                return cur.fetchone() is not None
        except Exception as e:
            logging.error(f"Error updating user admin status: {e}")
            return False
    
    def update_user_info(self, user_id: int, email: str = None, full_name: str = None, 
                        phone_number: str = None) -> bool:
        """Update user information"""
        query = """
            UPDATE users
            SET email = COALESCE(%s, email),
                full_name = COALESCE(%s, full_name),
                phone_number = COALESCE(%s, phone_number)
            WHERE id = %s
            RETURNING id
        """
        
        try:
            with self.get_cursor() as cur:
                cur.execute(query, (email, full_name, phone_number, user_id))
                return cur.fetchone() is not None
        except Exception as e:
            logging.error(f"Error updating user info: {e}")
            return False
    
    def update_user(self, user_id: int, username: str = None, email: str = None, 
                   full_name: str = None, phone_number: str = None, 
                   is_admin: bool = None, is_active: bool = None) -> Optional[Dict]:
        """Update user information comprehensively"""
        # Build dynamic query based on provided fields
        update_fields = []
        params = []
        
        if username is not None:
            # Check if username already exists for another user
            query_check = "SELECT id FROM users WHERE username = %s AND id != %s"
            try:
                with self.get_cursor() as cur:
                    cur.execute(query_check, (username, user_id))
                    if cur.fetchone():
                        raise ValueError(f"Username '{username}' already exists")
            except ValueError:
                raise
            except Exception as e:
                logging.error(f"Error checking username: {e}")
                raise
            
            update_fields.append("username = %s")
            params.append(username)
        
        if email is not None:
            update_fields.append("email = %s")
            params.append(email)
        
        if full_name is not None:
            update_fields.append("full_name = %s")
            params.append(full_name)
        
        if phone_number is not None:
            update_fields.append("phone_number = %s")
            params.append(phone_number)
        
        if is_admin is not None:
            update_fields.append("is_admin = %s")
            params.append(is_admin)
        
        if is_active is not None:
            update_fields.append("is_active = %s")
            params.append(is_active)
        
        if not update_fields:
            return self.get_user_by_id(user_id)
        
        params.append(user_id)
        query = f"""
            UPDATE users
            SET {', '.join(update_fields)}
            WHERE id = %s
            RETURNING id, username, email, full_name, phone_number, 
                     is_admin, is_active, last_login, created_by
        """
        
        try:
            with self.get_cursor() as cur:
                cur.execute(query, params)
                result = cur.fetchone()
                return dict(result) if result else None
        except Exception as e:
            logging.error(f"Error updating user: {e}")
            raise
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate a user"""
        query = """
            UPDATE users
            SET is_active = FALSE
            WHERE id = %s
            RETURNING id
        """
        
        try:
            with self.get_cursor() as cur:
                cur.execute(query, (user_id,))
                return cur.fetchone() is not None
        except Exception as e:
            logging.error(f"Error deactivating user: {e}")
            return False
    
    def remove_user_role(self, user_id: int, role_id: int) -> bool:
        """Remove a role from a user"""
        query = """
            DELETE FROM user_roles
            WHERE user_id = %s AND role_id = %s
            RETURNING id
        """
        
        try:
            with self.get_cursor() as cur:
                cur.execute(query, (user_id, role_id))
                return cur.fetchone() is not None
        except Exception as e:
            logging.error(f"Error removing user role: {e}")
            return False
    
    # ==================== DATABASE INITIALIZATION ====================
    
    def close_pool(self):
        """Close all connections in the pool"""
        try:
            self.pool.closeall()
            logging.info("Connection pool closed")
        except Exception as e:
            logging.error(f"Error closing connection pool: {e}")


# Export for easy import
if __name__ == "__main__":
    print("✅ AuthenticationManager module loaded successfully!")
    print("\n🔐 To authenticate, use:")
    print("   auth = AuthenticationManager()")
    print("   user = auth.authenticate_user('admin_user', 'admin123')")
