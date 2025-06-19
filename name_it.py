# name_it.py (updated)
import streamlit as st
import random
import time
from PIL import Image
from leaderboard import save_score

def show():
    st.markdown("<h2 style='color: #7e22ce;'>🧪 Name It! - IUPAC Challenge</h2>", unsafe_allow_html=True)

    questions = [
        # Image-based questions
        {"type": "image", "image": "methane.png", "question": "Name this compound:", "correct": "Methane", "options": ["Methane", "Ethane", "Propane", "Butane"]},
        {"type": "image", "image": "ethanol.png", "question": "Name this compound:", "correct": "Ethanol", "options": ["Propanol", "Methanol", "Ethanol", "Butanol"]},
        {"type": "image", "image": "propene.png", "question": "Name this compound:", "correct": "Propene", "options": ["Propyne", "Propene", "Propane", "Butene"]},
        {"type": "image", "image": "ethane.png", "question": "Name this compound:", "correct": "Ethane", "options": ["Methane", "Ethene", "Ethyne", "Ethane"]},
        {"type": "image", "image": "butane.png", "question": "Name this compound:", "correct": "Butane", "options": ["Butane", "Isobutane", "Butene", "Butyne"]},
        
        # Text-based questions
        {"type": "text", "question": "What is the IUPAC name for CH₃CH₂CH₂CH₃?", "correct": "Butane", "options": ["Methane", "Ethane", "Propane", "Butane"]},
        {"type": "text", "question": "Name the compound: CH₃CH₂OH", "correct": "Ethanol", "options": ["Methanol", "Ethanol", "Propanol", "Butanol"]},
        {"type": "text", "question": "What is the name of CH₃CH=CH₂?", "correct": "Propene", "options": ["Propane", "Propene", "Propyne", "Cyclopropane"]},
        {"type": "text", "question": "Name the compound: CH₃COOH", "correct": "Ethanoic acid", "options": ["Methanoic acid", "Ethanoic acid", "Propanoic acid", "Butanoic acid"]},
        {"type": "text", "question": "What is the IUPAC name for C₆H₆?", "correct": "Benzene", "options": ["Cyclohexane", "Benzene", "Hexene", "Hexane"]},
        {"type": "text", "question": "Name the compound: CH₃CH₂CH₂CHO", "correct": "Butanal", "options": ["Propanal", "Butanal", "Pentanone", "Butanol"]},
        {"type": "text", "question": "What is the IUPAC name for CH₃CH₂COCH₃?", "correct": "Butanone", "options": ["Propanone", "Butanone", "Pentanone", "Butanal"]},
        {"type": "text", "question": "Name the compound: CH₃CH₂OCH₂CH₃", "correct": "Ethoxyethane", "options": ["Methoxymethane", "Ethoxyethane", "Propoxypropane", "Butanol"]},
        {"type": "text", "question": "What is the name of CH₃CH₂NH₂?", "correct": "Ethanamine", "options": ["Methanamine", "Ethanamine", "Propanamine", "Butanamine"]},
        {"type": "text", "question": "Name the compound: CH₃CH₂CH₂CH₂CH₂COOH", "correct": "Hexanoic acid", "options": ["Pentanoic acid", "Hexanoic acid", "Heptanoic acid", "Octanoic acid"]},
    ]

    time_limit = 90  # Increased time limit
    total_questions = len(questions)

    if "name_it_start_time" not in st.session_state:
        st.session_state.name_it_score = 0
        st.session_state.name_it_index = 0
        st.session_state.name_it_questions = random.sample(questions, min(10, len(questions)))  # Show 10 random questions
        st.session_state.name_it_start_time = time.time()
        st.session_state.name_it_done = False
        st.session_state.name_it_submitted = False

    time_left = time_limit - int(time.time() - st.session_state.name_it_start_time)

    if st.session_state.name_it_done or time_left <= 0:
        if not st.session_state.name_it_done:
            st.session_state.name_it_done = True

        st.markdown(f"## ⏰ Time's up or quiz finished!")
        st.markdown(f"### 🏁 Final Score: **{st.session_state.name_it_score} / {len(st.session_state.name_it_questions)}**")

        if not st.session_state.name_it_submitted:
            name = st.text_input("Enter your name to save this score:", key="name_it_username")
            if st.button("💾 Submit to Leaderboard"):
                if name.strip():
                    save_score(name.strip(), "Name It!", st.session_state.name_it_score)
                    st.success("✅ Score submitted!")
                    st.session_state.name_it_submitted = True
                else:
                    st.warning("⚠️ Please enter your name.")
        if st.button("🔁 Restart Game"):
            for key in ["name_it_score", "name_it_index", "name_it_questions", "name_it_start_time", "name_it_done", "name_it_submitted"]:
                st.session_state.pop(key, None)
            st.rerun()
        return

    # Display timer and score
    col1, col2 = st.columns(2)
    with col1:
        st.metric("⏱️ Time Left", f"{time_left} seconds")
    with col2:
        st.metric("🏆 Score", f"{st.session_state.name_it_score}/{len(st.session_state.name_it_questions)}")

    # Display current question
    q = st.session_state.name_it_questions[st.session_state.name_it_index]
    
    st.markdown(f"### ❓ {q['question']}")
    
    if q['type'] == "image":
        st.image(f"assets/images/compounds/{q['image']}", width=300)
    
    answer = st.radio("Select your answer:", q["options"], key=f"q_{st.session_state.name_it_index}")

    if st.button("✅ Submit Answer"):
        if answer == q["correct"]:
            st.success("Correct! 🎉")
            st.session_state.name_it_score += 1
        else:
            st.error(f"Wrong! The correct answer is **{q['correct']}**")
        st.session_state.name_it_index += 1
        if st.session_state.name_it_index >= len(st.session_state.name_it_questions):
            st.session_state.name_it_done = True
        st.rerun()
