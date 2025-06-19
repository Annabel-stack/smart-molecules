# group_finder.py (updated)
import streamlit as st
import random
from PIL import Image

def show():
    st.markdown("<h2 style='color: #7e22ce;'>🔍 Functional Group Finder</h2>", unsafe_allow_html=True)

    questions = [
        {
            "clue": "This group contains an -OH bonded to a carbon.",
            "image": "alcohol.png",
            "correct": "Alcohol",
            "options": ["Alkane", "Alcohol", "Ester", "Alkyne"]
        },
        {
            "clue": "This group contains a C=C double bond.",
            "image": "alkene.png",
            "correct": "Alkene",
            "options": ["Alkene", "Alkyne", "Alkane", "Aromatic"]
        },
        {
            "clue": "This group contains a COOH group.",
            "image": "carboxylic_acid.png",
            "correct": "Carboxylic Acid",
            "options": ["Alcohol", "Ester", "Carboxylic Acid", "Ketone"]
        },
        {
            "clue": "This group has a COO linkage between carbon chains.",
            "image": "ester.png",
            "correct": "Ester",
            "options": ["Ether", "Alcohol", "Ester", "Amide"]
        },
        {
            "clue": "This group contains a C≡C triple bond.",
            "image": "alkyne.png",
            "correct": "Alkyne",
            "options": ["Alkene", "Alkyne", "Alkane", "Aromatic"]
        },
        {
            "clue": "This group has a C=O bond with two carbon attachments.",
            "image": "ketone.png",
            "correct": "Ketone",
            "options": ["Aldehyde", "Ketone", "Ester", "Carboxylic Acid"]
        },
        {
            "clue": "This group has a C=O bond with at least one hydrogen attachment.",
            "image": "aldehyde.png",
            "correct": "Aldehyde",
            "options": ["Aldehyde", "Ketone", "Alcohol", "Ether"]
        },
        {
            "clue": "This group has an oxygen between two carbon groups.",
            "image": "ether.png",
            "correct": "Ether",
            "options": ["Ester", "Ether", "Alcohol", "Ketone"]
        },
        {
            "clue": "This group contains a benzene ring structure.",
            "image": "aromatic.png",
            "correct": "Aromatic",
            "options": ["Alkene", "Alkyne", "Aromatic", "Ketone"]
        },
        {
            "clue": "This group contains a nitrogen atom with three bonds.",
            "image": "amine.png",
            "correct": "Amine",
            "options": ["Amide", "Amine", "Nitrile", "Amino Acid"]
        },
    ]

    # Session state
    if "fg_score" not in st.session_state:
        st.session_state.fg_score = 0
        st.session_state.fg_index = 0
        st.session_state.fg_questions = random.sample(questions, len(questions))
        st.session_state.fg_done = False

    # Game over logic
    if st.session_state.fg_done or st.session_state.fg_index >= len(st.session_state.fg_questions):
        st.markdown(f"### 🏁 Game Over! Final Score: **{st.session_state.fg_score} / {len(questions)}**")

        name = st.text_input("Enter your name for the leaderboard:", key="fg_name")
        if st.button("📩 Submit Score"):
            from leaderboard import save_score
            save_score(name.strip(), "Functional Group Finder", st.session_state.fg_score)
            st.success("✅ Score submitted!")

        if st.button("🔁 Play Again"):
            for key in ["fg_score", "fg_index", "fg_questions", "fg_name", "fg_done"]:
                st.session_state.pop(key, None)
            st.rerun()
        return

    # Regular question display
    q = st.session_state.fg_questions[st.session_state.fg_index]

    st.markdown(f"**Clue:** {q['clue']}")
    st.image(f"assets/images/functional_groups/{q['image']}", width=300)
    
    cols = st.columns(2)
    with cols[0]:
        answer = st.radio("Which functional group is this?", q["options"], key=f"fg_q_{st.session_state.fg_index}")
    with cols[1]:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("✅ Submit Answer"):
            if answer == q["correct"]:
                st.success("Correct! 🎉")
                st.session_state.fg_score += 1
            else:
                st.error(f"Wrong! The correct answer is {q['correct']}")
            st.session_state.fg_index += 1
            if st.session_state.fg_index >= len(st.session_state.fg_questions):
                st.session_state.fg_done = True
            st.rerun()
