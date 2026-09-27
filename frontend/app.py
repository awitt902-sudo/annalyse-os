import streamlit as st
import requests

st.set_page_config(page_title="AnnalyseOS Mission Control", page_icon="⚡", layout="wide")

API_BASE_URL = "http://localhost:8000/api/v1"

if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None


def auth_headers():
    if not st.session_state.token:
        return {}
    return {"Authorization": f"Bearer {st.session_state.token}"}


with st.sidebar:
    st.title("🔐 Authentication")
    if not st.session_state.token:
        auth_mode = st.radio("Mode", ["Login", "Register"], horizontal=True)
        with st.form("auth_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log In" if auth_mode == "Login" else "Register")
            if submitted:
                if auth_mode == "Login":
                    response = requests.post(f"{API_BASE_URL}/auth/token", data={"username": username, "password": password})
                    if response.status_code == 200:
                        st.session_state.token = response.json()["access_token"]
                        st.session_state.username = username
                        st.success("Logged in successfully")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    response = requests.post(f"{API_BASE_URL}/auth/register", json={"username": username, "password": password})
                    if response.status_code == 201:
                        st.success("Account created successfully")
                    else:
                        st.error(response.json().get("detail", "Registration failed"))
    else:
        st.success(f"Logged in as: {st.session_state.username}")
        if st.button("Log Out"):
            st.session_state.token = None
            st.session_state.username = None
            st.rerun()

st.title("🚀 AnnalyseOS Mission Control Dashboard")

if not st.session_state.token:
    st.warning("Please log in to access AnnalyseOS data.")
else:
    tabs = st.tabs(["Overview", "Scholarships", "Notes", "Projects"])

    with tabs[0]:
        try:
            response = requests.get(f"{API_BASE_URL}/mission-control/dashboard", headers=auth_headers())
            if response.status_code == 200:
                data = response.json()
                c1, c2, c3 = st.columns(3)
                c1.metric("Pending Scholarships", data["metrics"]["pending_scholarships_count"])
                c2.metric("Active Tasks", data["metrics"]["active_tasks_count"])
                c3.metric("Active Goals", data["metrics"]["active_goals_count"])
            else:
                st.error("Authentication failed")
        except requests.exceptions.ConnectionError:
            st.warning("Backend is not running. Start uvicorn main:app --reload")

    with tabs[1]:
        st.subheader("Scholarships")
        with st.form("scholarship_form"):
            title = st.text_input("Title")
            organization = st.text_input("Organization")
            amount = st.number_input("Amount", min_value=0.0, step=50.0)
            status = st.selectbox("Status", ["pending", "submitted", "awarded", "rejected"])
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Save Scholarship")
            if submitted:
                payload = {
                    "title": title,
                    "organization": organization,
                    "amount": amount,
                    "status": status,
                    "notes": notes,
                }
                res = requests.post(f"{API_BASE_URL}/scholarships/", json=payload, headers=auth_headers())
                if res.status_code == 201:
                    st.success("Saved")
                else:
                    st.error(res.text)

        res = requests.get(f"{API_BASE_URL}/scholarships/", headers=auth_headers())
        if res.status_code == 200:
            for item in res.json():
                st.write(f"- {item['title']} ({item['status']})")

    with tabs[2]:
        st.subheader("Notes")
        with st.form("note_form"):
            title = st.text_input("Note Title")
            category = st.text_input("Category")
            content = st.text_area("Content")
            pushed = st.form_submit_button("Save Note")
            if pushed:
                payload = {"title": title, "category": category, "content": content}
                res = requests.post(f"{API_BASE_URL}/notes/", json=payload, headers=auth_headers())
                if res.status_code == 201:
                    st.success("Saved")
                else:
                    st.error(res.text)

        res = requests.get(f"{API_BASE_URL}/notes/", headers=auth_headers())
        if res.status_code == 200:
            for item in res.json():
                st.write(f"## {item['title']}")
                st.write(item['content'])

    with tabs[3]:
        st.subheader("Projects")
        with st.form("project_form"):
            title = st.text_input("Project title")
            description = st.text_area("Description")
            tech_stack = st.text_input("Tech stack")
            submitted = st.form_submit_button("Save Project")
            if submitted:
                payload = {
                    "title": title,
                    "description": description,
                    "tech_stack": tech_stack,
                    "status": "active",
                }
                res = requests.post(f"{API_BASE_URL}/projects/", json=payload, headers=auth_headers())
                if res.status_code == 201:
                    st.success("Saved")
                else:
                    st.error(res.text)

        res = requests.get(f"{API_BASE_URL}/projects/", headers=auth_headers())
        if res.status_code == 200:
            for item in res.json():
                st.write(f"- {item['title']} ({item['status']})")
