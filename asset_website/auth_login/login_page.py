import streamlit as st
import sys
import os
from PIL import Image

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'auth_login'))

from database import AuthenticationManager

# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="Asset Management Login",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== CUSTOM CSS ====================

st.markdown("""
<style>
.login-card {
    background: #ffffff; 
    border-radius: 18px;
    padding: 40px 50px;
    width: 900px;
    min-height: 450px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.25);
    display: flex;
    gap: 40px;
}

            
* {
    margin: 0;
    padding: 0;
}
            
.button-wrapper button {
    margin-top: -10px !important;
}

html, body, [data-testid="stAppViewContainer"] {
    background: #0f0f1e;
}

[data-testid="stMainBlockContainer"] {
    padding: 0 !important;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

/* Page padding */
[data-testid="stAppViewContainer"] {
    padding-left: 10px !important;
    padding-right: 10px !important;
}

/* Reduce width of text input boxes */
.small-input input {
    width: 200px !important;
    height: 40px !important;
    padding: 8px 12px !important;
    font-size: 16px !important;
    border-radius: 8px !important;
}

/* Alternative: Target Streamlit input container */
.small-input [data-testid="stTextInput"] {
    max-width: 200px !important;
}

.small-input .stTextInput > div > div > input {
    width: 200px !important;
    max-width: 200px !important;
}

/* Reduce width of buttons */
.small-button button {
    width: 350px !important;
    height: 40px !important;
    font-size: 15px !important;
    border-radius: 8px !important;
}

/* Image styling */
.image-box img {
    width: 85%;
    max-width: 330px;
    border-radius: 12px;
}

.login-title {
    color: #fff;
    font-size: 3.5em;
    font-weight: 700;
    font-family: 'Arial', 'Helvetica', sans-serif;
    margin-bottom: 15px;
    margin-top: -10px;
}

.login-label {
    color: #ccc;
    font-size: 0.9em;
    margin-bottom: 5px;
    margin-top: 10px;
}

.page-container {
    margin-left: 100px;
}
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.user_id = None

# ==================== LOAD IMAGE ====================

def load_login_image():
    """Load the login page image from auth_login folder"""
    image_path = os.path.join(
        os.path.dirname(__file__), 
        '..', 
        'auth_login', 
        'image.png'
    )
    
    if os.path.exists(image_path):
        try:
            return Image.open(image_path)
        except Exception as e:
            st.error(f"Error loading image: {e}")
            return None
    else:
        st.warning(f"Image not found at: {image_path}")
        return None

# ==================== AUTHENTICATION FUNCTIONS ====================

def authenticate(username: str, password: str):
    """Authenticate user with username and password"""
    try:
        auth = AuthenticationManager()
        user = auth.authenticate_user(username, password)
        auth.close_pool()
        
        if user:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.session_state.user_id = user['id']
            return True, "Login successful!"
        else:
            return False, "Invalid username or password"
    except Exception as e:
        return False, f"Error: {str(e)}"

# ==================== LOGIN PAGE ====================

def login_page():
    """Render login page with image and form side by side"""

    # Center title at top
    st.markdown('<div class="login-title" style="text-align: center;">Valve 360</div>', unsafe_allow_html=True)

    # Add empty column on left for spacing (100px effect)
    spacer, col1, col2 = st.columns([0.43, 0.75, 1], gap="large")

    # LEFT (IMAGE)
    with col1:
        img = load_login_image()
        if img:
            st.markdown('<div class="image-box">', unsafe_allow_html=True)
            st.image(img, use_container_width=False)
            st.markdown('</div>', unsafe_allow_html=True)

    # RIGHT (FORM)
    with col2:
        # Add spacing at top
        st.markdown('<div style="margin-top: 50px;"></div>', unsafe_allow_html=True)
        
        # Username field
        username_col, _ = st.columns([0.6, 0.5])
        with username_col:
            username = st.text_input("Username", placeholder="Enter your username", label_visibility="collapsed")
    
        # Password field
        password_col, _ = st.columns([0.6, 0.5])
        with password_col:
            password = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)
    
        msg = st.empty()
    
        # Login button
        st.markdown('<div class="button-wrapper">', unsafe_allow_html=True)

        # Login button
        login_clicked = st.button("Login")
        
        # Move Guest button UP or DOWN relative to Login
        st.markdown('<div style="height:-20px;"></div>', unsafe_allow_html=True)
        
        # Guest button
        st.button("Continue as Guest", disabled=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

        if login_clicked:
            if not username or not password:
                msg.error("Please enter both username and password")
            else:
                with st.spinner("Logging in..."):
                    success, message = authenticate(username, password)
                    if success:
                        msg.success(message)
                        st.balloons()
                        st.rerun()
                    else:
                        msg.error(message)

# ==================== MAIN APP ====================

def main():
    """Main app logic"""
    if st.session_state.logged_in:
        st.success(f"Logged in as {st.session_state.user['username']}. Dashboard coming soon...")
    else:
        login_page()

if __name__ == "__main__":
    main()
