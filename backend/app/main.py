from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="NHJ AI", version="0.3.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

users = [
    {"id": "u-1001", "name": "أحمد العتيبي", "role": "admin", "email": "admin@nhj.ai", "active": True},
    {"id": "u-1002", "name": "سارة المهنا", "role": "project_manager", "email": "pm@nhj.ai", "active": True},
    {"id": "u-1003", "name": "محمد البسام", "role": "engineer", "email": "eng@nhj.ai", "active": True},
]

projects = [
    {"id": "NHJ-001", "name": "مجمع النخيل السكني", "owner": "شركة البناء المتحدة", "progress": 78, "status": "active"},
    {"id": "NHJ-002", "name": "مستشفى المدينة الطبي", "owner": "مؤسسة الإعمار", "progress": 52, "status": "active"},
    {"id": "NHJ-003", "name": "مركز الأعمال الذكي", "owner": "شركة نهج للمقاولات", "progress": 31, "status": "planning"},
]

procurement = [
    {"id": "PO-1048", "project_id": "NHJ-001", "description": "مواد بناء", "quantity": 240, "status": "approved"},
    {"id": "PO-1049", "project_id": "NHJ-002", "description": "ألواح إنارة", "quantity": 340, "status": "requested"},
]

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: str = Field(min_length=5, max_length=120)
    role: str = Field(default="user")

class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    owner: str = Field(min_length=2, max_length=120)
    progress: int = Field(default=0, ge=0, le=100)
    status: str = Field(default="planning")

class ProcurementCreate(BaseModel):
    project_id: str
    description: str = Field(min_length=2, max_length=160)
    quantity: float = Field(gt=0)
    status: str = Field(default="requested")

@app.get("/")
def root() -> dict[str, str]:
    return {"message": "NHJ AI API is running", "version": app.version}

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "NHJ AI Backend"}

@app.get("/api/dashboard")
def dashboard() -> dict:
    return {
        "projects": len(projects),
        "procurement": len(procurement),
        "active_projects": sum(item["status"] == "active" for item in projects),
        "users": len(users),
    }

@app.get("/api/users")
def list_users() -> list[dict]:
    return users

@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate) -> dict:
    user = {"id": f"u-{len(users) + 1001}", **payload.model_dump(), "active": True}
    users.append(user)
    return user

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
    item = {"id": f"PO-{len(procurement) + 1048}", **payload.model_dump()}
    procurement.append(item)
    return item
