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

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs

On first startup the app auto-creates the SQLite schema and seeds:
- default roles (admin, project_manager, engineer, ai_agent, estimator, procurement, verifier, auditor)
- default units of measure + conversions
- an admin user only when `ADMIN_INITIAL_PASSWORD` is set in `backend/.env`; no password is embedded in source code

The `/users` screen is the admin-only management console for adding members, changing roles, editing profile data, enabling/disabling accounts, and resetting passwords. New or reset accounts must change their password at first login.

## Status note

This was built without network access in the sandbox, so dependencies
could not be `pip install`-ed and the server could not actually be
booted here. Every file passed `python -m py_compile` (no syntax
errors), and the code was reviewed end-to-end — in that review three
real bugs were caught and fixed (SQLAlchemy `Date`/`DateTime` column
types used where the Python `date`/`datetime` type was needed in
`Mapped[...]` annotations, in `takeoff.py`, `pricing.py`, and
`procurement.py`). That said, this has not been run, so treat the
first `uvicorn` launch on your machine as the real first test —
please report anything that breaks.

## Design notes worth knowing before you extend this

- **RBAC**: permissions are a flat JSON list per role (`app/models/user.py`,
  `DEFAULT_ROLES`) rather than a normalized permission table — enough for
  v0.1, easy to swap later without touching `User`.
- **Engineer Takeoff immutability**: a takeoff header owns an ordered set
  of revisions. Locking a revision (`POST /engineer-takeoffs/{id}/lock`)
  is enforced only in `services/takeoff_service.py` — there is no DB-level
  trigger preventing writes to a locked revision, so any new code path
  that touches `EngineerTakeoffLine` directly must go through that service.
- **Blind VERIFY**: the "blind" guarantee is an API-response contract, not
  a DB constraint — `VerificationLineBlindRead` simply omits
  `engineer_qty`/`ai_qty` until `verifier_qty` is set. Anyone querying the
  DB directly bypasses this.
- **Audit log**: append-only by convention (no route or service issues
  UPDATE/DELETE against `audit_logs`) — again not DB-enforced.
- Migrations: not set up yet. `Base.metadata.create_all()` runs on
  startup, which is fine for v0.1/SQLite but should be replaced with
  Alembic before PostgreSQL/production.
