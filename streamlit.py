# streamlit.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("TutorAIPortal/.env")
API_BASE = os.getenv("API_BASE", "http://localhost:5000")  # Adjust if your backend runs elsewhere

st.set_page_config(page_title="Tutor AI Portal", page_icon="🎓", layout="centered")

st.title("🎓 Tutor AI Portal")

# Session state for login persistence
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "token" not in st.session_state:
    st.session_state.token = None

def login(username, password):
    try:
        response = requests.post(
            f"{API_BASE}/api/login",
            json={"username": username, "password": password},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()  # e.g. { "token": "xyz" }
        else:
            st.error(f"Login failed: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Login Form
if not st.session_state.logged_in:
    with st.form("login_form"):
        st.subheader("Login to continue")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            result = login(username, password)
            if result and "token" in result:
                st.session_state.logged_in = True
                st.session_state.token = result["token"]
                st.success("✅ Login successful! Reloading...")
                st.experimental_rerun()

else:
    st.success("✅ Logged in successfully!")
    st.write("Welcome to the **Tutor AI Portal Dashboard** 🎉")

    # Example protected API call
    if st.button("Fetch My Profile"):
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        try:
            r = requests.get(f"{API_BASE}/api/profile", headers=headers)
            if r.status_code == 200:
                st.json(r.json())
            else:
                st.error(f"Error fetching profile: {r.text}")
        except Exception as e:
            st.error(f"Error: {e}")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.token = None
        st.experimental_rerun()
