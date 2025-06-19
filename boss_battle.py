import streamlit as st
import random
from leaderboard import save_score

def show():
    st.markdown("<h2 style='color: #7e22ce;'>🧪 Organic Boss Battle</h2>", unsafe_allow_html=True)
    st.markdown("Defeat the reaction monster by answering correctly!")

    questions = [
        {"question": "What is the functional group in CH₃COOH?", "correct": "Carboxylic Acid", "options": ["Alcohol", "Ester", "Carboxylic Acid", "Ketone"]},
        {"question": "Name the compound: CH₃CH=CH₂", "correct": "Propene", "options": ["Propane", "Propene", "Propyne", "Propanol"]},
        {"question": "Which is an isomer of butane?", "correct": "Methylpropane", "options": ["Methane", "Propane", "Ethanol", "Methylpropane"]},
        {"question": "Type of reaction: CH₃CH=CH₂ + Br₂", "correct": "Addition", "options": ["Substitution", "Elimination", "Addition", "Combustion"]},
        {"question": "Functional group with C=C?", "correct": "Alkene", "options": ["Alkyne", "Alkane", "Alkene", "Aromatic"]},
        {"question": "Product of: CH₃COOH + CH₃OH", "correct": "Methyl ethanoate", "options": ["Methanol", "Ethanol", "Methyl ethanoate", "Acetone"]},
        {"question": "What is the general formula of alkanes?", "correct": "CnH2n+2", "options": ["CnH2n", "CnH2n+1", "CnH2n+1OH", "CnHn"]},
        {"question": "What type of bond is present in alkanes?", "correct": "Single covalent(sigma) bonds", "options": ["Double bond", "Triple bond", "quadruple bond", "ionic bond"]},
        {"question": "", "correct": "Hydrocarbon", "options": ["Aliphatic compounds", "Carbon compounds", "Carbon hydrolysis", "Petroleum"]},
        {"question": "An organic compound which reacts readily with bromine to form a compound with the formula CH2CHBrCH2Br is:", "correct": "Propene", "options": ["Ethene", "Propane", "Butane", "Toluene"]},
        {"question": "Thermal cracking of alkanes usually:", "correct": "involves decomposition", "options": ["is an exothermic processs", "produces only small alkanes", "requires hydrogen", "is an endothermic process"]},
        {"question": "An example of a carboxylic acid is ___________", "correct": "Acetic acid", "options": ["Propylnoic acid", "Ethyl Butanoate", "Butane", "Ethanol"]},
        {"question": "Name the process by which alkenes are converted to alkanes", "correct": "Hydrogenation", "options": ["Electrolysis", "Hydrolysis", "Dehydration", "Halogenation"]},
        {"question": "What is the hybridization of carbon in ethyne(C2H2)", "correct": "sp hybridization", "options": ["sp3 hybridization", "Tetrahedral hybridization", "sp2 hybridization", "Linear hybridization"]},
        {"question": "What is the IUPAC name of CH3CH=CH2", "correct": "Propene", "options": ["Ethene", "2-dimethylpropane", "But-2-ene", "Pentene"]}
    ]

    # Initialize game state
    if "boss_hp" not in st.session_state:
        st.session_state.boss_hp = 100
        st.session_state.player_hp = 3
        st.session_state.boss_index = 0
        st.session_state.boss_score = 0
        st.session_state.boss_questions = random.sample(questions, len(questions))
        st.session_state.boss_done = False
        st.session_state.boss_submitted = False

    # Game over logic
    if st.session_state.boss_done or st.session_state.player_hp <= 0 or st.session_state.boss_hp <= 0:
        outcome = "🏆 You defeated the Boss!" if st.session_state.boss_hp <= 0 else "💀 You were defeated!"
        st.markdown(f"### {outcome}")
        st.markdown(f"**Final Score:** {st.session_state.boss_score} points")

        if not st.session_state.boss_submitted:
            name = st.text_input("Enter your name to save your battle score:", key="boss_name")
            if st.button("📩 Submit to Leaderboard"):
                if name.strip():
                    save_score(name.strip(), "Organic Boss Battle", st.session_state.boss_score)
                    st.success("✅ Score saved!")
                    st.session_state.boss_submitted = True
                else:
                    st.warning("Please enter your name.")

        if st.button("🔁 Retry Boss Battle"):
            for key in ["boss_hp", "player_hp", "boss_index", "boss_score", "boss_questions", "boss_done", "boss_submitted"]:
                st.session_state.pop(key, None)
            st.rerun()
        return

    # Show current boss/player status
    st.progress(st.session_state.boss_hp / 100)
    st.markdown(f"🧪 **Boss HP:** {st.session_state.boss_hp}")
    st.markdown(f"❤️ **Your Lives:** {st.session_state.player_hp}")
    st.markdown(f"🔥 **Your Score:** {st.session_state.boss_score}")

        # Prevent crash if questions are done
    if st.session_state.boss_index >= len(st.session_state.boss_questions):
        st.session_state.boss_done = True
        st.rerun()
        return

    q = st.session_state.boss_questions[st.session_state.boss_index]

    st.markdown(f"**Question {st.session_state.boss_index + 1}:** {q['question']}")
    answer = st.radio("Choose your answer:", q["options"], key=f"boss_q_{st.session_state.boss_index}")

    if st.button("⚔️ Attack!"):
        if answer == q["correct"]:
            st.success("Hit! 🎯 You dealt 20 damage!")
            st.session_state.boss_hp -= 20
            st.session_state.boss_score += 1
        else:
            st.error(f"Miss! 😓 The correct answer was: {q['correct']}")
            st.session_state.player_hp -= 1

        st.session_state.boss_index += 1
        if st.session_state.boss_index >= len(st.session_state.boss_questions):
            st.session_state.boss_done = True
        st.rerun()
