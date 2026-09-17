# NHJ AI v0.1

Executable foundation for the NHJ AI construction platform.

## v0.1 scope

- FastAPI backend
- SQLite development database (PostgreSQL-ready SQLAlchemy)
- Authentication + RBAC
- Project Core
- Project document metadata
- Engineer Takeoff with immutable lock/revision model
- Independent AI Takeoff
- Calculation/conversion engine
- Blind VERIFY
- Pricing foundation
- PR/PO/GRN/Material Issue foundations
- Approval workflow foundation
- Append-only Audit Log

## Run

\`\`\`bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
\`\`\`

API docs: http://127.0.0.1:8000/docs

On first startup the app auto-creates the SQLite schema and seeds:
- default roles (admin, project_manager, engineer, ai_agent, estimator, procurement, verifier, auditor)
- default units of measure + conversions
- an admin user only when `ADMIN_INITIAL_PASSWORD` is set in `backend/.env`; no password is embedded in source code

The `/users` screen is the admin-only management console for adding members, changing roles, editing profile data, enabling/disabling accounts, and resetting passwords. New or reset accounts must change their password at first
