# NHJ AI

This repository contains a working starter foundation for the NHJ AI platform.

## Stack

- Frontend: Next.js (App Router)
- Backend: FastAPI

## Quick start

### Frontend

```bash
git clone https://github.com/nhjalbunian-tech/NHJ.git
cd NHJ
corepack enable
pnpm install
pnpm dev
```

Open http://localhost:3000

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open http://127.0.0.1:8000/docs

## Notes

- The frontend and backend are separated intentionally for clean development.
- The code here is a usable foundation, not a full production ERP implementation.
- The backend is intentionally minimal and ready to expand with auth, project, procurement, and takeoff modules.
