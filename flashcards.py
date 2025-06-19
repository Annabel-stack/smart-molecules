import streamlit as st
import random
import os

def load_flashcards(path):
    with open(path, "r", encoding="utf-8") as f:
        entries = f.read().split("\n\n")
        cards = []
        for entry in entries:
            lines = entry.strip().split("\n")
            if len(lines) == 2 and lines[0].startswith("Q:") and lines[1].startswith("A:"):
                q = lines[0][3:].strip()
                a = lines[1][3:].strip()
                cards.append((q, a))
        return cards

def show():
    st.markdown("<h2 style='color: #7e22ce;'>🧠 Organic Chemistry Flashcards</h2>", unsafe_allow_html=True)

    flashcard_dir = "assets/flashcards"
    files = [f for f in os.listdir(flashcard_dir) if f.endswith(".txt")]

    if not files:
        st.warning("⚠️ No flashcard files found in the folder.")
        return

    topic_names = [f.replace("_cards.txt", "") for f in files]
    topic = st.selectbox("Select a topic:", topic_names)
    file_path = f"{flashcard_dir}/{topic}_cards.txt"

    cards = load_flashcards(file_path)
    if not cards:
        st.warning("⚠️ No valid flashcards found in the file.")
        return

    if "fc_index" not in st.session_state or st.session_state.get("fc_topic") != topic:
        st.session_state.fc_index = 0
        st.session_state.fc_show_answer = False
        st.session_state.fc_topic = topic
        random.shuffle(cards)

    q, a = cards[st.session_state.fc_index]
    show_answer = st.session_state.fc_show_answer
    bg_color = "#f3e8ff" if not show_answer else "#ddd6fe"
    content = f"❓ {q}" if not show_answer else f"✅ {a}"

    st.markdown(
        f"""
        <div style='background-color: {bg_color}; padding: 30px; border-radius: 20px; text-align: center;
        font-size: 20px; color: #1e1b4b; font-weight: bold;'>
        {content}
        </div>
        """, unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    if col1.button("🔄 Flip"):
        st.session_state.fc_show_answer = not st.session_state.fc_show_answer
    if col2.button("➡️ Next"):
        st.session_state.fc_index = (st.session_state.fc_index + 1) % len(cards)
        st.session_state.fc_show_answer = False
