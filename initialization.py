import os

def initialize_directories():
    # Create necessary directories if they don't exist
    os.makedirs("assets/flashcards", exist_ok=True)
    os.makedirs("assets/notes", exist_ok=True)
    os.makedirs("assets/images/functional_groups", exist_ok=True)
    os.makedirs("assets/images/isomers", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Create empty leaderboard file if it doesn't exist
    if not os.path.exists("data/leaderboard.csv"):
        import pandas as pd
        pd.DataFrame(columns=["Name", "Game", "Score"]).to_csv("data/leaderboard.csv", index=False)

if __name__ == "__main__":
    initialize_directories()
