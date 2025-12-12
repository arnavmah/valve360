"""
User Activity Tab for Admin Panel
Handles user activity monitoring and logs
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from auth_login.database import AuthenticationManager


class UserActivityTab:
    """User Activity Tab - Monitor user activities and system usage"""
    
    def __init__(self, auth_manager: AuthenticationManager):
        """
        Initialize User Activity tab
        
        Args:
            auth_manager: AuthenticationManager instance for database operations
        """
        self.auth = auth_manager
    
    def render(self):
        """Render the User Activity tab"""
        st.header("📊 User Activity")
        st.write("Monitor user activities and system usage.")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Fetch data for summary statistics
        daily_stats = self.auth.get_daily_login_stats(days=30)
        all_users = self.auth.get_all_users()
        
        # Calculate summary statistics
        total_users = len(all_users)
        active_users = len([u for u in all_users if u.get('last_login') is not None])
        
        # Calculate average daily logins and latest day's login count
        if daily_stats:
            total_logins = sum(stat['success_count'] for stat in daily_stats)
            avg_daily_logins = total_logins / len(daily_stats) if daily_stats else 0
            latest_day_logins = daily_stats[0]['success_count'] if daily_stats else 0
        else:
            avg_daily_logins = 0
            latest_day_logins = 0
        
        # Display summary statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="👥 Total Users",
                value=total_users
            )
        
        with col2:
            st.metric(
                label="✅ Active Users",
                value=active_users
            )
        
        with col3:
            st.metric(
                label="📈 Avg Daily Logins",
                value=f"{avg_daily_logins:.1f}"
            )
        
        with col4:
            st.metric(
                label="📅 Today's Logins",
                value=latest_day_logins
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ==================== CHART 1: DAILY LOGINS LINE CHART ====================
        st.subheader("📈 Daily Successful Logins")
        
        if daily_stats:
            # Prepare data for the line chart
            df_daily = pd.DataFrame(daily_stats)
            # Sort by date in ascending order for proper line chart display
            df_daily = df_daily.sort_values('date_stamp')
            
            # Create line chart using Plotly Express
            fig_daily = px.line(
                df_daily,
                x='date_stamp',
                y='success_count',
                title='System-Wide Activity Over Time',
                labels={
                    'date_stamp': 'Date',
                    'success_count': 'Successful Logins'
                },
                markers=True
            )
            
            # Update layout to match Streamlit theme
            fig_daily.update_layout(
                xaxis_title="Date",
                yaxis_title="Number of Successful Logins",
                hovermode='x unified',
                showlegend=False,
                height=400,
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            # Update trace style
            fig_daily.update_traces(
                line=dict(color='#1f77b4', width=2.5),
                marker=dict(size=6, color='#1f77b4')
            )
            
            # Display the chart
            st.plotly_chart(fig_daily, use_container_width=True)
        else:
            st.info("No daily login data available yet.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ==================== CHART 2: TOP USERS BAR CHART ====================
        st.subheader("🏆 Top Active Users by Login Count")
        
        # Add filter for top N users
        col_filter1, col_filter2 = st.columns([1, 3])
        with col_filter1:
            top_n = st.selectbox(
                "Show top:",
                options=[5, 10, 15, 20],
                index=1,  # Default to 10
                key="top_users_filter"
            )
        
        # Fetch top users data
        top_users = self.auth.get_top_users_by_login_count(limit=top_n)
        
        if top_users:
            # Prepare data for bar chart
            df_top_users = pd.DataFrame(top_users)
            
            # Create bar chart using Plotly Express
            fig_top_users = px.bar(
                df_top_users,
                x='username',
                y='login_count',
                title=f'Top {top_n} Users with Highest Number of Logins',
                labels={
                    'username': 'Username',
                    'login_count': 'Total Login Count'
                },
                text='login_count'
            )
            
            # Update layout to match Streamlit theme
            fig_top_users.update_layout(
                xaxis_title="Username",
                yaxis_title="Total Login Count",
                showlegend=False,
                height=450,
                margin=dict(l=50, r=50, t=80, b=50),
                xaxis={'categoryorder': 'total descending'}
            )
            
            # Update bar style
            fig_top_users.update_traces(
                marker_color='#ff7f0e',
                textposition='outside'
            )
            
            # Display the chart
            st.plotly_chart(fig_top_users, use_container_width=True)
        else:
            st.info("No login data available yet.")
