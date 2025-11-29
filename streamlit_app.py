# Root-level entry point for Streamlit Cloud deployment
# This file simply runs the main app from the StudyBuddy directory

import sys
sys.path.insert(0, 'StudyBuddy')

# Import and run the main app
from streamlit_app import *
