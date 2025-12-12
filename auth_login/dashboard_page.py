import streamlit as st
import sys
import os
import time
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
                'change': '5%',
                'label': 'SINCE LAST MONTH',
            },
            'pipelines': {
                'value': 3006,
                'change': '-4.54%',
                'label': 'SINCE LAST MONTH',
            },
            'terminals': {
                'value': '60%',
                'change': '2.64%',
                'label': 'SINCE LAST MONTH',
            },
            'assets': {
                'value': 852,
                'change': '6.84%',
                'label': 'SINCE LAST MONTH',
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
    
    def __init__(self):
        """Initialize dashboard page"""
        self.dashboard_manager = DashboardManager()
    
    def _render_sidebar(self):
        """Render sidebar with welcome message and admin controls"""
        with st.sidebar:
            user = st.session_state.get('user', {})
            username = user.get('username', 'User')
            is_admin = user.get('is_admin', False)
            
            st.title("Values 360")
            st.markdown(f"👋 Welcome, **{username}**")
            st.markdown("---")
            
            # Admin Controls - Only show if user is admin
            if is_admin:
                st.subheader("🔒 Admin Controls")
                
                # Admin Panel Button
                if st.button("⚙️ Admin Panel", key="admin_panel_btn", use_container_width=True):
                    st.session_state.current_page = "admin_panel"
                    st.rerun()
                
                st.divider()
            
            # Navigation Section
            st.subheader("📋 Navigation")
            
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
            
            # Logout button
            if st.button("🚪 Logout", type="primary", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.session_state.user_id = None
                st.rerun()
    
    def _render_metrics(self):
        """Render dashboard metrics with beautiful cards that work in both light and dark modes"""
        metrics = self.dashboard_manager.get_dashboard_metrics()
        
        # Define icon mappings for each metric
        metric_icons = {
            'organizations': '🏢',
            'pipelines': '🔩━🛢️',
            'terminals': '🖥️ ➤',
            'assets': '💼'
        }
        
        # Custom CSS for beautiful metric cards
        st.markdown("""
        <style>
        .metric-card {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.12) 0%, rgba(6, 182, 212, 0.08) 100%);
            border-radius: 16px;
            padding: 16px 20px;
            border: 1px solid rgba(59, 130, 246, 0.25);
            transition: all 0.3s ease;
            margin-bottom: 16px;
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
        }
        
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 32px rgba(59, 130, 246, 0.25);
            border-color: rgba(59, 130, 246, 0.4);
        }
        
        .metric-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 8px;
        }
        
        .metric-icon {
            font-size: 40px;
            opacity: 0.85;
        }
        
        .metric-title {
            font-size: 15px;
            font-weight: 600;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            opacity: 0.75;
            margin-bottom: -2px;
        }
        
        .metric-value {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 4px;
            background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .metric-change {
            display: flex;
            align-items: center;
            font-size: 15px;
            font-weight: 500;
            margin-top: -2px;
        }
        
        .metric-change.positive {
            color: #00d4aa;
        }
        
        .metric-change.negative {
            color: #ff6b9d;
        }
        
        .metric-label {
            font-size: 11px;
            opacity: 0.65;
            margin-left: 8px;
            letter-spacing: 0.6px;
        }
        
        /* Dark mode specific adjustments */
        @media (prefers-color-scheme: dark) {
            .metric-card {
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.18) 0%, rgba(6, 182, 212, 0.12) 100%);
                border-color: rgba(59, 130, 246, 0.3);
            }
            
            .metric-card:hover {
                box-shadow: 0 12px 36px rgba(59, 130, 246, 0.35);
            }
        }
        
        /* Light mode specific adjustments */
        @media (prefers-color-scheme: light) {
            .metric-card {
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(6, 182, 212, 0.06) 100%);
                border-color: rgba(59, 130, 246, 0.2);
            }
            
            .metric-title, .metric-label {
                opacity: 0.65;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create 4 columns for the metric cards
        cols = st.columns(4)
        
        for idx, (key, data) in enumerate(metrics.items()):
            title = key.replace('_', ' ').upper()
            icon = metric_icons.get(key, '📊')
            
            # Determine if change is positive or negative
            change_value = data['change']
            is_positive = not change_value.startswith('-')
            change_class = 'positive' if is_positive else 'negative'
            change_symbol = '▲' if is_positive else '▼'
            
            # Format value - handle both numbers and strings
            value = data['value']
            if isinstance(value, (int, float)):
                formatted_value = f"{value:,.0f}"
            else:
                formatted_value = str(value)
            
            with cols[idx]:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-header">
                        <div class="metric-title">{title}</div>
                        <div class="metric-icon">{icon}</div>
                    </div>
                    <div class="metric-value">{formatted_value}</div>
                    <div class="metric-change {change_class}">
                        <span>{change_symbol} {change_value}</span>
                        <span class="metric-label">{data['label']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
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
        
        # Add custom CSS for header and tab styling
        st.markdown("""
        <style>
        /* Header Styling - Simple with underline */
        .dashboard-header {
            margin-bottom: 28px;
        }
        
        .dashboard-header h1 {
            font-size: 2.25rem;
            font-weight: 600;
            letter-spacing: -0.025em;
            margin: 0;
            padding: 0;
            margin-bottom: 8px;
        }
        
        .header-underline {
            height: 3px;
            width: 64px;
            border-radius: 9999px;
            background: linear-gradient(to right, #3b82f6, #06b6d4);
            margin-top: 4px;
        }
        
        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border-radius: 8px;
            padding: 10px 20px;
            transition: all 0.3s ease;
            color: inherit !important;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(59, 130, 246, 0.1);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%);
            color: inherit !important;
        }
        
        .stTabs [aria-selected="true"]::after {
            background-color: #3b82f6 !important;
        }
        
        .stTabs [data-baseweb="tab-highlight"] {
            background-color: #3b82f6 !important;
        }
        
        .stTabs [data-baseweb="tab"] p {
            color: inherit !important;
        }
        
        .stTabs [aria-selected="true"] p {
            color: inherit !important;
        }
        
        /* Dark mode adjustments */
        @media (prefers-color-scheme: dark) {
            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(6, 182, 212, 0.15) 100%);
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # App Header with simple underline design
        st.markdown("""
        <div class="dashboard-header">
            <h1>Valve 360 Dashboard</h1>
            <div class="header-underline"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs
        tab1, tab2 = st.tabs(["📊 Data Management", "🔍 Entity Overview"])
        
        with tab1:
            # Data Management Tab - Show metric cards
            st.subheader("Key Metrics")
            self._render_metrics()
        
        with tab2:
            # Entity Overview Tab - Blank for now
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
