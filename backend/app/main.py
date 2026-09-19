from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="NHJ AI", version="0.2.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

projects: list[dict] = [
    {"id": "NHJ-001", "name": "مجمع النخيل السكني", "owner": "شركة البناء المتحدة", "progress": 78, "status": "active"},
    {"id": "NHJ-002", "name": "مستشفى المدينة الطبي", "owner": "مؤسسة الإعمار", "progress": 52, "status": "active"},
]
procurement: list[dict] = []

class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    owner: str = Field(min_length=2, max_length=120)
    progress: int = Field(default=0, ge=0, le=100)
    status: Literal["planning", "active", "completed"] = "planning"

class ProcurementCreate(BaseModel):
    project_id: str
    description: str = Field(min_length=2, max_length=200)
    quantity: float = Field(gt=0)
    status: Literal["requested", "approved", "received"] = "requested"

@app.get("/")
def root() -> dict[str, str]:
    return {"message": "NHJ AI API is running", "version": app.version}

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "NHJ AI Backend"}

@app.get("/api/dashboard")
def dashboard() -> dict:
    return {"projects": len(projects), "procurement": len(procurement), "active_projects": sum(item["status"] == "active" for item in projects), "updated_at": datetime.now(timezone.utc).isoformat()}

@app.get("/api/projects")
def list_projects() -> list[dict]:
    return projects

@app.post("/api/projects", status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate) -> dict:
    project = {"id": f"NHJ-{len(projects) + 1:03d}", **payload.model_dump()}
    projects.append(project)
    return project

@app.get("/api/procurement")
def list_procurement() -> list[dict]:
    return procurement

@app.post("/api/procurement", status_code=status.HTTP_201_CREATED)
def create_procurement(payload: ProcurementCreate) -> dict:
    if not any(item["id"] == payload.project_id for item in projects):
        raise HTTPException(status_code=404, detail="Project not found")
    item = {"id": str(uuid4()), **payload.model_dump()}
    procurement.append(item)
    return item
