import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from auth_login.login_page import LoginApp

def main():
    """Main entry point for the Streamlit app"""
    app = LoginApp()
    app.run()

if __name__ == "__main__":
    main()