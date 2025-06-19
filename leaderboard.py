# leaderboard.py (updated)
import streamlit as st
import pandas as pd
import os
from auth import show_auth

LEADERBOARD_FILE = "data/leaderboard.csv"

def load_leaderboard():
    os.makedirs(os.path.dirname(LEADERBOARD_FILE), exist_ok=True)
    
    if not os.path.exists(LEADERBOARD_FILE) or os.path.getsize(LEADERBOARD_FILE) == 0:
        df = pd.DataFrame(columns=["Name", "Username", "Game", "Score"])
        df.to_csv(LEADERBOARD_FILE, index=False)
        return df
    
    try:
        return pd.read_csv(LEADERBOARD_FILE)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=["Name", "Username", "Game", "Score"])
        df.to_csv(LEADERBOARD_FILE, index=False)
        return df

def save_score(name, game, score):
    df = load_leaderboard()
    username = st.session_state.get("current_user", "guest")
    new_entry = pd.DataFrame([[name, username, game, score]], columns=["Name", "Username", "Game", "Score"])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(LEADERBOARD_FILE, index=False)

def show():
    st.markdown("<h2 style='color: #7e22ce;'>🏆 Leaderboard</h2>", unsafe_allow_html=True)
    
    try:
        df = load_leaderboard()
        
        if df.empty:
            st.info("No scores yet. Be the first to play!")
        else:
            # Show overall leaderboard
            st.markdown("### Overall Top Scores")
            df_sorted = df.sort_values(by="Score", ascending=False).head(10)
            st.dataframe(df_sorted.reset_index(drop=True), hide_index=True)
            
            # Show game-specific leaderboards
            games = df['Game'].unique()
            selected_game = st.selectbox("View scores for specific game:", games)
            
            game_scores = df[df['Game'] == selected_game].sort_values(by="Score", ascending=False).head(10)
            st.markdown(f"### Top {selected_game} Scores")
            st.dataframe(game_scores.reset_index(drop=True), hide_index=True)

    except Exception as e:
        st.error(f"Error loading leaderboard: {str(e)}")
        df = pd.DataFrame(columns=["Name", "Username", "Game", "Score"])
        df.to_csv(LEADERBOARD_FILE, index=False)
        st.info("Created a new leaderboard. No scores yet.")

    with st.expander("📩 Submit your score"):
        name = st.text_input("Enter your name:")
        game = st.selectbox("Which game did you play?", 
                          ["Name It!", "Functional Group Finder", "Reaction Master", 
                           "Isomer Game", "Organic Boss Battle"])
        score = st.number_input("Your score:", min_value=0, step=1)

        if st.button("Submit Score"):
            if not name.strip():
                st.warning("Please enter your name.")
            else:
                save_score(name.strip(), game, score)
                st.success("🎉 Score submitted!")
                st.rerun()
