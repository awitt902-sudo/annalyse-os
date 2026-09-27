import os

import requests
import streamlit as st

st.set_page_config(page_title="AnnalyseOS Mission Control", page_icon="⚡", layout="wide")

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1").rstrip("/")

if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None


def auth_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"} if st.session_state.token else {}


def api_request(method, path, **kwargs):
    try:
        return requests.request(method, f"{API_BASE_URL}{path}", timeout=15, **kwargs)
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the FastAPI backend. Start uvicorn main:app --reload.")
    except requests.exceptions.Timeout:
        st.error("The API request timed out.")
    return None


def handle_auth_error(response):
    if response is not None and response.status_code == 401:
        st.session_state.token = None
        st.session_state.username = None
        st.warning("Your session expired. Please log in again.")
        st.rerun()


with st.sidebar:
    st.title("🔐 Authentication")
    if not st.session_state.token:
        mode = st.radio("Mode", ["Login", "Register"], horizontal=True)
        with st.form("auth_form"):
            username = st.text_input("Username", min_chars=3)
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log In" if mode == "Login" else "Register")
            if submitted:
                if mode == "Login":
                    response = api_request("POST", "/auth/token", data={"username": username, "password": password})
                    if response is not None and response.status_code == 200:
                        st.session_state.token = response.json()["access_token"]
                        st.session_state.username = username
                        st.rerun()
                    elif response is not None:
                        st.error(response.json().get("detail", "Invalid username or password"))
                else:
                    response = api_request("POST", "/auth/register", json={"username": username, "password": password})
                    if response is not None and response.status_code == 201:
                        st.success("Account created. Switch to Login.")
                    elif response is not None:
                        st.error(response.json().get("detail", "Registration failed"))
    else:
        st.success(f"Logged in as: {st.session_state.username}")
        if st.button("Log Out", use_container_width=True):
            st.session_state.token = None
            st.session_state.username = None
            st.rerun()

st.title("🚀 AnnalyseOS Mission Control Dashboard")

if not st.session_state.token:
    st.info("Register or log in from the sidebar to access the dashboard.")
else:
    overview, scholarships, notes, projects = st.tabs(["Overview", "Scholarships", "Notes", "Projects"])

    with overview:
        response = api_request("GET", "/mission-control/dashboard", headers=auth_headers())
        if response is not None:
            handle_auth_error(response)
            if response.status_code == 200:
                data = response.json()
                c1, c2, c3 = st.columns(3)
                c1.metric("Pending Scholarships", data["metrics"]["pending_scholarships_count"])
                c2.metric("Active Tasks", data["metrics"]["active_tasks_count"])
                c3.metric("Active Goals", data["metrics"]["active_goals_count"])

    with scholarships:
        st.subheader("🎓 Scholarships")
        with st.form("scholarship_form"):
            title = st.text_input("Title")
            organization = st.text_input("Organization")
            amount = st.number_input("Amount", min_value=0.0, step=50.0)
            status = st.selectbox("Status", ["pending", "submitted", "awarded", "rejected"])
            notes_text = st.text_area("Notes")
            submitted = st.form_submit_button("Save Scholarship")
            if submitted:
                response = api_request("POST", "/scholarships/", json={"title": title, "organization": organization, "amount": amount, "status": status, "notes": notes_text}, headers=auth_headers())
                if response is not None and response.status_code == 201:
                    st.success("Scholarship saved.")
                elif response is not None:
                    handle_auth_error(response)
                    st.error(response.text)
        response = api_request("GET", "/scholarships/", headers=auth_headers())
        if response is not None and response.status_code == 200:
            for item in response.json():
                st.write(f"- **{item['title']}** — {item.get('status', 'pending')}")

    with notes:
        st.subheader("📝 Technical Notes")
        with st.form("note_form"):
            title = st.text_input("Note Title")
            category = st.text_input("Category", value="General")
            content = st.text_area("Content")
            submitted = st.form_submit_button("Save Note")
            if submitted:
                response = api_request("POST", "/notes/", json={"title": title, "category": category, "content": content}, headers=auth_headers())
                if response is not None and response.status_code == 201:
                    st.success("Note saved.")
                elif response is not None:
                    handle_auth_error(response)
                    st.error(response.text)
        response = api_request("GET", "/notes/", headers=auth_headers())
        if response is not None and response.status_code == 200:
            for item in response.json():
                with st.expander(item["title"]):
                    st.caption(item.get("category", "General"))
                    st.write(item["content"])

    with projects:
        st.subheader("💻 Projects")
        with st.form("project_form"):
            title = st.text_input("Project Title")
            description = st.text_area("Description")
            tech_stack = st.text_input("Tech Stack")
            repository_url = st.text_input("Repository URL")
            submitted = st.form_submit_button("Save Project")
            if submitted:
                response = api_request("POST", "/projects/", json={"title": title, "description": description, "tech_stack": tech_stack, "repository_url": repository_url, "status": "active"}, headers=auth_headers())
                if response is not None and response.status_code == 201:
                    st.success("Project saved.")
                elif response is not None:
                    handle_auth_error(response)
                    st.error(response.text)
        response = api_request("GET", "/projects/", headers=auth_headers())
        if response is not None and response.status_code == 200:
            for item in response.json():
                st.write(f"- **{item['title']}** — {item.get('status', 'active')}")
