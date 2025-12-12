"""
Shared CSS styles for the admin panel
"""

# Shared CSS styles for consistent blue theme across admin panel
CSS_STYLES = """
<style>
/* Tab Styling - Blue Theme */
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
"""
