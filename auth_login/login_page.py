import streamlit as st
import sys
import os
from PIL import Image
from auth_login.database import AuthenticationManager


class LoginManager:
    """Handles authentication logic"""
    
    def __init__(self):
        self.auth = AuthenticationManager()
    
    def authenticate(self, username: str, password: str) -> tuple[bool, str, dict | None]:
        """Authenticate user with username and password"""
        try:
            user = self.auth.authenticate_user(username, password)
            self.auth.close_pool()
            
            if user:
                return True, "Login successful!", user
            else:
                return False, "Invalid username or password", None
        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    def set_session_state(self, user: dict):
        """Set user session state"""
        st.session_state.logged_in = True
        st.session_state.user = user
        st.session_state.user_id = user['id']


class LoginPage:
    """Handles login page UI and rendering"""
    
    def __init__(self, image_path: str = None):
        """Initialize login page with optional custom image path"""
        self.image_path = image_path or os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'auth_login', 
            'image.png'
        )
        self.login_manager = LoginManager()
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state"""
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.user_id = None
    
    def _load_image(self) -> Image.Image | None:
        """Load the login page image"""
        if os.path.exists(self.image_path):
            try:
                return Image.open(self.image_path)
            except Exception as e:
                st.error(f"Error loading image: {e}")
                return None
        else:
            # st.warning(f"Image not found at: {self.image_path}")
            return None
    
    def _render_login_form(self) -> tuple[str, str, bool]:
        """Render login form and return username, password, and login button state"""
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            login_clicked = st.form_submit_button("Login", use_container_width=True)
        
        st.button("Continue as Guest", disabled=True, use_container_width=True)
        
        return username, password, login_clicked
    
    def render(self):
        """Render the complete login page"""
        
        st.title("Valve 360")

        # Stable layout: Image on top/side depending on screen, form below
        # Using a simple 2-column layout with equal width
        col1, col2 = st.columns(2)

        # LEFT (IMAGE)
        with col1:
            img = self._load_image()
            if img:
                st.image(img, use_container_width=True)

        # RIGHT (FORM)
        with col2:
            st.header("Login")
            username, password, login_clicked = self._render_login_form()
            msg = st.empty()

            if login_clicked:
                if not username or not password:
                    msg.error("Please enter both username and password")
                else:
                    with st.spinner("Logging in..."):
                        success, message, user = self.login_manager.authenticate(username, password)
                        if success:
                            self.login_manager.set_session_state(user)
                            msg.success(message)
                            st.balloons()
                            st.rerun()
                        else:
                            msg.error(message)
    
class LoginApp:
    """Main application class"""
    
    def __init__(self, image_path: str = None):
        """Initialize the login app"""
        self.login_page = LoginPage(image_path)
    
    def run(self):
        """Run the login app"""
        self.login_page.render()


# ==================== MAIN ENTRY POINT ====================

if __name__ == "__main__":
    app = LoginApp()
    app.run()
