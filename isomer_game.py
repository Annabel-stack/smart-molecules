# isomer_game.py (final working version)
import streamlit as st
import random

def show():
    st.markdown("<h2 style='color: #7e22ce;'>🔁 Isomer Game</h2>", unsafe_allow_html=True)
    st.markdown("Identify the correct isomer for each compound!")

    # Define questions with consistent structure
    questions = [
        {
            "type": "text",
            "question": "Which of these is a structural isomer of butane (C₄H₁₀)?",
            "correct": "2-methylpropane",
            "options": ["Propane", "Butene", "2-methylpropane", "Cyclobutane"],
            "explanation": "2-methylpropane (isobutane) has the same molecular formula (C₄H₁₀) as butane but a different structure."
        },
        {
            "type": "text", 
            "question": "Which is a functional group isomer of ethanol (CH₃CH₂OH)?",
            "correct": "Dimethyl ether",
            "options": ["Methanol", "Ethanoic acid", "Dimethyl ether", "Ethene"],
            "explanation": "Dimethyl ether (CH₃OCH₃) has the same molecular formula (C₂H₆O) as ethanol but different functional groups."
        },
        {
            "type": "image",
            "question": "Which is a positional isomer of pentan-2-one?",
            "base_image": "pentan2one.png",
            "correct": "Pentan-3-one",
            "options": [
                {"image": "pentan3one.png", "label": "Pentan-3-one", "correct": True},
                {"image": "pentanal.png", "label": "Pentanal", "correct": False},
                {"image": "cyclopentanone.png", "label": "Cyclopentanone", "correct": False}
            ],
            "explanation": "Pentan-3-one has the carbonyl group at position 3 instead of position 2."
        }
    ]

    # Initialize game state
    if "iso_index" not in st.session_state:
        st.session_state.iso_index = 0
        st.session_state.iso_score = 0
        st.session_state.iso_questions = random.sample(questions, len(questions))
        st.session_state.iso_done = False

    # Game over logic
    if st.session_state.iso_done or st.session_state.iso_index >= len(st.session_state.iso_questions):
        st.markdown(f"### 🏁 Final Score: {st.session_state.iso_score} / {len(st.session_state.iso_questions)}")
        
        name = st.text_input("Enter your name to save to leaderboard:", key="iso_name")
        if st.button("📩 Submit Score"):
            from leaderboard import save_score
            save_score(name.strip(), "Isomer Game", st.session_state.iso_score)
            st.success("✅ Score submitted!")
        
        if st.button("🔁 Play Again"):
            for key in ["iso_index", "iso_score", "iso_questions", "iso_name", "iso_done"]:
                st.session_state.pop(key, None)
            st.rerun()
        return

    # Get current question
    q = st.session_state.iso_questions[st.session_state.iso_index]

    # Display question
    st.markdown(f"### ❓ Question {st.session_state.iso_index + 1}")
    st.markdown(f"**{q['question']}**")
    
    # Display base image if this is an image question
    if q["type"] == "image" and "base_image" in q:
        st.image(f"assets/images/isomers/{q['base_image']}", width=250)

    # Display options based on question type
    if q["type"] == "text":
        answer = st.radio("Select your answer:", q["options"], key=f"iso_q_{st.session_state.iso_index}")
    else:
        # For image questions
        cols = st.columns(3)
        selected = None
        for i, opt in enumerate(q["options"]):
            with cols[i % 3]:
                st.image(f"assets/images/isomers/{opt['image']}", caption=opt["label"], width=150)
                if st.button(f"Select {opt['label']}", key=f"select_{i}"):
                    selected = opt["label"]

    if q["type"] == "text":
        if st.button("✅ Submit Answer"):
            if answer == q["correct"]:
                st.success("Correct! 🎉")
                st.session_state.iso_score += 1
            else:
                st.error(f"Incorrect! The correct answer is: {q['correct']}")
            st.markdown(f"**Explanation:** {q['explanation']}")
            st.session_state.iso_index += 1
            if st.session_state.iso_index >= len(st.session_state.iso_questions):
                st.session_state.iso_done = True
            st.rerun()
    else:
        if selected:
            correct_option = next(opt for opt in q["options"] if opt["correct"])
            if selected == correct_option["label"]:
                st.success("Correct! 🎉")
                st.session_state.iso_score += 1
            else:
                st.error(f"Incorrect! The correct answer is: {correct_option['label']}")
            st.markdown(f"**Explanation:** {q['explanation']}")
            st.session_state.iso_index += 1
            if st.session_state.iso_index >= len(st.session_state.iso_questions):
                st.session_state.iso_done = True
            st.rerun()
