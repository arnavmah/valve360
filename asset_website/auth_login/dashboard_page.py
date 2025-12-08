import streamlit as st
import sys
import os
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
                'change': '+5%',
                'label': 'SINCE LAST MONTH',
                'icon': '🏢',
                'color': '#1a1a2e'
            },
            'pipelines': {
                'value': 3006,
                'change': '-4.54%',
                'label': 'SINCE LAST MONTH',
                'icon': '🔩━🛢️',
                'color': '#16213e'
            },
            'terminals': {
                'value': '60%',
                'change': '+2.64%',
                'label': 'SINCE LAST MONTH',
                'icon': '🖥️ ➤',
                'color': '#0f3460'
            },
            'assets': {
                'value': 852,
                'change': '+6.84%',
                'label': 'SINCE LAST MONTH',
                'icon': '💼',
                'color': '#533483'
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
    
    /* Dashboard Title */
    .dashboard-title {
        color: #fff;
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 30px;
        font-family: 'Arial', 'Helvetica', sans-serif;
    }
    
    /* Metric Cards Container */
    .metric-cards-container {
        display: flex;
        gap: 25px;
        margin-top: 30px;
        flex-wrap: wrap;
    }
    
    /* Individual Metric Card */
    .metric-card {
        flex: 1;
        min-width: 250px;
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.9) 0%, rgba(22, 33, 62, 0.9) 100%);
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .metric-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .metric-title {
        color: #fff;
        font-size: 0.85em;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-icon {
        font-size: 2em;
        opacity: 0.8;
    }
    
    .metric-value {
        color: #fff;
        font-size: 2.5em;
        font-weight: 700;
        margin: 10px 0;
        line-height: 1;
    }
    
    .metric-footer {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 15px;
    }
    
    .metric-change {
        font-size: 0.9em;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 6px;
    }
    
    .metric-change.positive {
        color: #4ade80;
        background: rgba(74, 222, 128, 0.1);
    }
    
    .metric-change.negative {
        color: #f87171;
        background: rgba(248, 113, 113, 0.1);
    }
    
    .metric-label {
        color: #9ca3af;
        font-size: 0.75em;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Logout Button */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Admin Controls Section */
    .admin-section {
        background: rgba(255, 165, 0, 0.1);
        border-left: 3px solid #ffa500;
        padding: 8px;
        margin: 8px 0;
        border-radius: 6px;
    }
    
    .admin-section h3 {
        color: #ffa500;
        font-size: 1.1em;
        margin-bottom: 8px;
        font-weight: 600;
    }
    
    /* Section Headers with Grey Glow */
    [data-testid="stSidebar"] h3 {
        color: #e0e0e0;
        text-shadow: 0 0 5px rgba(224, 224, 224, 0.2);
        font-size: 1.1em;
        font-weight: 600;
        margin: 8px 0 8px 0;
    }
    
    /* Navigation Boxes - Even Shorter and More Compact */
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
    }
    
    .stButton > button:hover {
        background: #3a3a4e !important;
        border-color: rgba(102, 126, 234, 0.5) !important;
        transform: translateX(3px) !important;
    }
    
    /* Purple Styling for Admin Panel and Logout Buttons */
    .stButton > button[key="admin_panel_btn"],
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
    }
    
    .stButton > button[key="admin_panel_btn"]:hover,
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #7a8ef0 0%, #8a5bb8 100%) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    </style>
    """
    
    def __init__(self):
        """Initialize dashboard page"""
        self.dashboard_manager = DashboardManager()
        self._apply_styles()
    
    def _apply_styles(self):
        """Apply custom CSS styles"""
        st.markdown(self.CSS_STYLES, unsafe_allow_html=True)
    
    def _render_sidebar(self):
        """Render sidebar with welcome message and admin controls"""
        with st.sidebar:
            user = st.session_state.get('user', {})
            username = user.get('username', 'User')
            is_admin = user.get('is_admin', False)
            
            st.markdown(f"# 👋 Welcome")
            st.markdown(f"### {username}")
            st.markdown("---")
            
            # Admin Controls - Only show if user is admin
            if is_admin:
                st.markdown('<div class="admin-section">', unsafe_allow_html=True)
                st.markdown("### 🔒 Admin Controls")
                
                # Admin Panel Button
                if st.button("⚙️ Admin Panel", key="admin_panel_btn"):
                    st.session_state.current_page = "admin_panel"
                    st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Navigation Section
            st.markdown("### 📋 Go to")
            
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
            
            # Logout button with purple styling
            if st.button("🚪 Logout", type="primary"):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.session_state.user_id = None
                st.rerun()
    
    def _render_metric_card(self, title: str, data: Dict) -> str:
        """Generate HTML for a metric card"""
        change_class = 'positive' if '+' in data['change'] else 'negative'
        
        return f"""
        <div class="metric-card">
            <div class="metric-card-header">
                <div class="metric-title">{title}</div>
                <div class="metric-icon">{data['icon']}</div>
            </div>
            <div class="metric-value">{data['value']:,}</div>
            <div class="metric-footer">
                <div class="metric-change {change_class}">{data['change']}</div>
                <div class="metric-label">{data['label']}</div>
            </div>
        </div>
        """
    
    def _render_metrics(self):
        """Render dashboard metrics using Streamlit columns"""
        metrics = self.dashboard_manager.get_dashboard_metrics()
        
        # Create 4 columns for the metric cards
        cols = st.columns(4)
        
        for idx, (key, data) in enumerate(metrics.items()):
            title = key.replace('_', ' ').title()
            change_class = 'positive' if '+' in data['change'] else 'negative'
            
            with cols[idx]:
                # Create HTML for each metric card
                card_html = f"""
                <div class="metric-card">
                    <div class="metric-card-header">
                        <div class="metric-title">{title}</div>
                        <div class="metric-icon">{data['icon']}</div>
                    </div>
                    <div class="metric-value">{data['value'] if isinstance(data['value'], str) else f"{data['value']:,}"}</div>
                    <div class="metric-footer">
                        <div class="metric-change {change_class}">{data['change']}</div>
                        <div class="metric-label">{data['label']}</div>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
    
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
        st.markdown('''
            <div class="app-header">
                <h1>Valve 360</h1>
            </div>
        ''', unsafe_allow_html=True)
        
        # Create tabs
        tab1, tab2 = st.tabs(["📊 Data Management", "🔍 Entity Overview"])
        
        with tab1:
            # Data Management Tab - Show metric cards
            st.markdown("<br>", unsafe_allow_html=True)
            self._render_metrics()
        
        with tab2:
            # Entity Overview Tab - Blank for now
            st.markdown("<br>", unsafe_allow_html=True)
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
