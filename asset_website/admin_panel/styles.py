"""
Shared CSS styles for the admin panel
"""

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
