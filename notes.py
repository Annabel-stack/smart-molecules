import streamlit as st
import os

def show():
    st.markdown("<h2 style='color: #7e22ce;'>📘 Organic Chemistry Notes</h2>", unsafe_allow_html=True)
    st.write("Select a topic below to view notes:")

    notes_dir = "assets/notes"
    topics = [f.replace(".md", "") for f in os.listdir(notes_dir) if f.endswith(".md")]

    selected = st.selectbox("🧪 Choose a topic:", topics)

    if selected:
        filepath = f"{notes_dir}/{selected}.md"
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        st.markdown(
            f"""
            <div style='background-color: #f3e8ff; padding: 20px; border-radius: 15px;'>
            {content}
            </div>
            """, unsafe_allow_html=True
        )
