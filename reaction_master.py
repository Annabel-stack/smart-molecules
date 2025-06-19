import streamlit as st
import random

def show():
    st.markdown("<h2 style='color: #7e22ce;'>⚗️ Reaction Master</h2>", unsafe_allow_html=True)

    questions = [
        {
            "question": "What is the product of: Ethene + H₂ → ?",
            "correct": "Ethane",
            "options": ["Ethane", "Ethanol", "Ethanoic acid", "Propane"]
        },
        {
            "question": "CH₃COOH + CH₃OH → ?",
            "correct": "Methyl ethanoate",
            "options": ["Methanol", "Ethanoic acid", "Methyl ethanoate", "Acetone"]
        },
        {
            "question": "Which type of reaction is: alkane + halogen (in UV)?",
            "correct": "Substitution",
            "options": ["Substitution", "Addition", "Combustion", "Neutralization"]
        },
        {
            "question": "Alkene + Br₂ results in what kind of reaction?",
            "correct": "Addition",
            "options": ["Addition", "Substitution", "Elimination", "Oxidation"]
        },
        {
            "question":"The reaction between an organic acid and an alcohol in the presence of an acid catalyst is known as________",
            "correct":"Esterification",
            "options":["Saponification", "Dehydration", "Hydrolysis", "Hydration"]
        },
        {
            "question":"The type of reaction that is peculiar to benzene is?",
            "correct":"Substitution",
            "options":["Elimination", "Polymerization", "Addition", "Hydrolysis"]
        },
        {
            "question":"A substance that is used as a ripening agent for fruits is_________",
            "correct":"Etheyne",
            "options":["Ethane", "Ethyl", "Ethene", "Ethanol"]
        },
        {
            "question":"An organic compound reacted with bromine water to give a colourless solution. The compound is probably an?",
            "correct":"Alkene",
            "options":["Alkanal", "Alkyl", "Alkanone", "Amide"]
        },
        {
            "question":"Which of the following compounds reacts with sodium hydroxide to form a salt?",
            "correct":"CH3CH=CH2",
            "options":["(CH3)3COH","CH3CH=CH2","C6H12O6","CH3CH2"]
        },
        {
            "question":"2-methylprop-1-ene is an isomer of?",
            "correct":"but-2-ene",
            "options":["3-methyl but-1-ene","2-methyl but-1-ene","pent-2-ene","ethyl propanoate"]
        },
        {
            "question":"The IUPAC name of the compound CH2=CH-CCL=CH2 is ?",
            "correct":"2-chlorobut-1,3-diene",
            "options":["But-1,3-chlorodiene","2-chlorobut-diene","3-chlorobut-1,3-diene","2-dichloromethyl"]
        },
        {
            "question":"Give the common name for the following compound (CH3)2CHCH2Br",
            "correct":"Isobutyl bromide",
            "options":["Methyl bromide","Propyl bromide","Butyl bromide","Ethyl bromide"]
        },
        {
            "question":"The enzyme that converts glucose to ethyl alcohol is?",
            "correct":"Zymase",
            "options":["Maltase","Diatase","Invertase","Maltose"]
        },
        {
            "question":"What is the IUPAC name for the compound HC≡CCH3",
            "correct":"Methyl acetylene",
            "options":["Acetylene","Butanol","Decanoic acid","Glycerol"]
        }
    ]

    if "rm_index" not in st.session_state:
        st.session_state.rm_index = 0
        st.session_state.rm_score = 0
        st.session_state.rm_questions = random.sample(questions, len(questions))
        st.session_state.rm_done = False
        st.session_state.rm_submitted = False

    # ✅ Handle game end BEFORE trying to access a question
    if st.session_state.rm_index >= len(st.session_state.rm_questions) or st.session_state.rm_done:
        st.markdown(f"## 🧪 Quiz Complete!")
        st.markdown(f"### 🏁 Final Score: {st.session_state.rm_score} / {len(st.session_state.rm_questions)}")

        if not st.session_state.rm_submitted:
            name = st.text_input("Enter your name for the leaderboard:", key="rm_name")
            if st.button("📩 Submit Score"):
                if name.strip():
                    from leaderboard import save_score
                    save_score(name.strip(), "Reaction Master", st.session_state.rm_score)
                    st.success("✅ Score submitted!")
                    st.session_state.rm_submitted = True
                else:
                    st.warning("Please enter a valid name.")

        if st.button("🔄 Restart"):
            for key in ["rm_index", "rm_score", "rm_questions", "rm_name", "rm_done", "rm_submitted"]:
                st.session_state.pop(key, None)
            st.rerun()
        return

    # 🔽 Safe to show question now
    q = st.session_state.rm_questions[st.session_state.rm_index]
    st.markdown(f"### ❓ {q['question']}")
    answer = st.radio("Choose your answer:", q["options"], key=f"rm_q{st.session_state.rm_index}")

    if st.button("✅ Submit"):
        if answer == q["correct"]:
            st.success("Correct! 🎉")
            st.session_state.rm_score += 1
        else:
            st.error(f"Incorrect! The correct answer is: {q['correct']}")
        st.session_state.rm_index += 1
        if st.session_state.rm_index >= len(st.session_state.rm_questions):
            st.session_state.rm_done = True
        st.rerun()
