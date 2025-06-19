# auth.py
import streamlit as st
import pandas as pd
import hashlib
import os

USER_DATA_FILE = "data/users.csv"

def initialize_auth():
    os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)
    if not os.path.exists(USER_DATA_FILE):
        pd.DataFrame(columns=["username", "password", "name", "level"]).to_csv(USER_DATA_FILE, index=False)

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

def register_user(username, password, name, level="student"):
    df = pd.read_csv(USER_DATA_FILE)
    if username in df['username'].values:
        return False
    hashed_pswd = make_hashes(password)
    new_user = pd.DataFrame([[username, hashed_pswd, name, level]], 
                          columns=["username", "password", "name", "level"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_DATA_FILE, index=False)
    return True

def login_user(username, password):
    df = pd.read_csv(USER_DATA_FILE)
    if username in df['username'].values:
        hashed_pswd = df[df['username'] == username]['password'].values[0]
        return check_hashes(password, hashed_pswd)
    return False

def show_auth():
    st.sidebar.image("assets/logo.png", width=150)
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.current_user = None
    
    if not st.session_state.authenticated:
        auth_type = st.sidebar.radio("", ["Login", "Register"])
        
        if auth_type == "Login":
            with st.sidebar.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    if login_user(username, password):
                        st.session_state.authenticated = True
                        st.session_state.current_user = username
                        st.sidebar.success(f"Welcome back, {username}!")
                        st.rerun()
                    else:
                        st.sidebar.error("Invalid credentials")
        
        else:  # Registration
            with st.sidebar.form("register_form"):
                st.markdown("### New User Registration")
                new_username = st.text_input("Choose a username")
                new_name = st.text_input("Your full name")
                new_password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                
                if st.form_submit_button("Register"):
                    if new_password != confirm_password:
                        st.sidebar.error("Passwords don't match!")
                    elif register_user(new_username, new_password, new_name):
                        st.sidebar.success("Registration successful! Please login.")
                    else:
                        st.sidebar.error("Username already exists")
    else:
        st.sidebar.success(f"Logged in as {st.session_state.current_user}")
        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.rerun()
    
    return st.session_state.authenticated
