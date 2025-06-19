# app.py (updated)
import os
import sys
from pathlib import Path
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from auth import show_auth, initialize_auth

# Ensure local imports work
sys.path.insert(0, str(Path(__file__).parent.resolve()))

# Initialize directories and authentication
def initialize():
    os.makedirs("assets/flashcards", exist_ok=True)
    os.makedirs("assets/notes", exist_ok=True)
    os.makedirs("assets/images/functional_groups", exist_ok=True)
    os.makedirs("assets/images/isomers", exist_ok=True)
    os.makedirs("assets/images/compounds", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    if not os.path.exists("data/leaderboard.csv"):
        pd.DataFrame(columns=["Name", "Username", "Game", "Score"]).to_csv("data/leaderboard.csv", index=False)
    
    initialize_auth()

# Run initialization
initialize()

# Apply custom theme
st.set_page_config(
    page_title="Smart Molecules",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f9f5ff;
    }
    .sidebar .sidebar-content {
        background-color: #f3e8ff;
        background-image: linear-gradient(to bottom, #7e22ce, #a855f7);
    }
    .block-container {
        padding-top: 2rem;
    }
    .stButton>button {
        background-color: #7e22ce;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #6b21a8;
        color: white;
    }
    .stRadio>div>div {
        background-color: #f3e8ff;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Show authentication
if not show_auth():
    st.warning("Please login or register to continue")
    st.stop()

# Import modules after authentication
try:
    from app_splash import show as splash_show
    import notes
    import flashcards
    import name_it
    import group_finder
    import reaction_master
    import isomer_game
    import boss_battle
    import leaderboard
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.stop()

# Splash screen only once
if "splash_shown" not in st.session_state:
    splash_show()
    st.session_state.splash_shown = True

# Sidebar menu
with st.sidebar:
    st.markdown("## Smart Molecules")
    st.caption("🌟 Where molecules meet mastery")

    selected = option_menu(
        "Main Menu",
        ["Home", "Notes", "Flashcards", "Name It!", " Group Finder",
         "Reaction Master", "Isomer Game", "Boss Battle", "Leaderboard"],
        icons=["house", "book", "card-text", "pencil", "search", "lightning-charge", "shuffle","joystick", "trophy"],
        menu_icon="menu-app",
        default_index=0,
        styles={
            "container": {"padding": "5px"},
            "icon": {"color": "white", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "#6b21a8"},
        }
    )

# Navigation logic
if selected == "Home":
    st.markdown("## 🧬 Welcome to Smart Molecules!")
    st.markdown("Your interactive platform for mastering organic chemistry concepts through engaging tools and games.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("assets/logo.png", width=200)
    with col2:
        st.markdown("""
        ### Key Features:
        - 📚 **Comprehensive Notes** - Detailed organic chemistry concepts
        - 🎴 **Interactive Flashcards** - Reinforce your learning
        - 🎮 **Educational Games** - Fun way to test your knowledge
        - 🏆 **Leaderboard** - Compete with peers
        """)
    
    st.markdown("---")
    
    st.markdown("### 🔥 Popular Learning Tools")
    cols = st.columns(3)
    with cols[0]:
        st.markdown("""
        #### Name It!
        Test your IUPAC naming skills with visual and text-based questions.
        """)
    with cols[1]:
        st.markdown("""
        #### Reaction Master
        Predict organic reaction products and types.
        """)
    with cols[2]:
        st.markdown("""
        #### Boss Battle
        Challenge yourself with progressively harder questions.
        """)
    
    st.markdown("---")
    st.markdown("💡 Built with Python and Streamlit for SS2 Science Project.")
    
elif selected == "Notes":
    notes.show()
elif selected == "Flashcards":
    flashcards.show()
elif selected == "Name It!":
    name_it.show()
elif selected == "Functional Group Finder":
    group_finder.show()
elif selected == "Reaction Master":
    reaction_master.show()
elif selected == "Isomer Game":
    isomer_game.show()
elif selected == "Organic Boss Battle":
    boss_battle.show()
elif selected == "Leaderboard":
    leaderboard.show()

