import streamlit as st
import time

def show():  # Consistent naming with other modules
    st.markdown("<h1 style='text-align: center; color: purple;'>Smart Molecules</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Where molecules meet</h3>", unsafe_allow_html=True)
    st.image("assets/logo.png", width=200)
    with st.spinner('🔬 Initializing molecules...'):
        time.sleep(2)
    st.success("Loaded! Let's learn chemistry 💥")
