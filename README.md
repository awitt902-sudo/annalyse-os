# AnnalyseOS

AnnalyseOS is a modular systems engineering and workflow platform built to organize scholarship tracking, personal goals, project logs, technical notes, and operational priorities in one place.

## Overview

This project combines:
- FastAPI backend for secure API services
- SQLAlchemy ORM for persistent data storage
- Pydantic validation for clean request/response contracts
- JWT-based authentication and role-based access control
- Streamlit frontend for a mission-control dashboard
- GitHub Actions-ready project structure for automation

## Goals

- Track scholarships, deadlines, and award status
- Organize technical notes and project documentation
- Consolidate active goals and tasks into a single dashboard
- Demonstrate backend architecture and systems thinking in a portfolio
- Create a foundation for future cloud deployment and automation work

## Repository Layout

```text
annalyse-os/
├── main.py
├── config.py
├── requirements.txt
├── .gitignore
├── README.md
├── database/
│   ├── __init__.py
│   ├── base.py
│   └── session.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── scholarship.py
│   ├── task.py
│   ├── goal.py
│   ├── project.py
│   └── note.py
├── schemas/
│   ├── __init__.py
│   ├── user.py
│   ├── scholarship.py
│   ├── task.py
│   ├── goal.py
│   ├── project.py
│   └── note.py
├── services/
│   ├── __init__.py
│   ├── scholarship_service.py
│   └── mission_control_service.py
├── api/
│   ├── __init__.py
│   ├── auth.py
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── scholarships.py
│       ├── notes.py
│       ├── projects.py
│       └── mission_control.py
├── frontend/
│   └── app.py
├── docs/
│   └── ARCHITECTURE.md
└── .env.example
```

## Local Development

1. Create and activate a virtual environment
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the backend:

```bash
uvicorn main:app --reload
```

4. Launch the Streamlit app in another terminal:

```bash
streamlit run frontend/app.py
```

## Default Routes

- API docs: http://localhost:8000/docs
- Streamlit dashboard: http://localhost:8501

## Security Notes

- Keep `.env` and production secrets out of GitHub
- Use JWT-based auth for protected routes
- Keep private research and WIP work separate from public portfolio repositories

## Author

Awitt902-sudo
