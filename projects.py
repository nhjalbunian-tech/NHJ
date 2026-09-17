from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_permission
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.services import audit_service

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("project:create")),
) -> Project:
    if db.query(Project).filter(Project.code == payload.code).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Project code already exists")

    project = Project(**payload.model_dump(), created_by_id=user.id)
    db.add(project)
    db.flush()
    audit_service.record(
        db, entity_type="project", entity_id=project.id, action="create",
        actor_id=user.id, after=payload.model_dump(),
    )
    db.commit()
    db.refresh(project)
    return project


@router.get("", response_model=list[ProjectRead])
def list_projects(
    db: Session = Depends(get_db), _user: User = Depends(require_permission("project:read"))
) -> list[Project]:
    return db.query(Project).all()


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(
    project_id: str, db: Session = Depends(get_db), _user: User = Depends(require_permission("project:read"))
) -> Project:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: str,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("project:update")),
) -> Project:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")

    before = {"name": project.name, "status": project.status.value}
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, field, value)

    audit_service.record(
        db, entity_type="project", entity_id=project.id, action="update",
        actor_id=user.id, before=before, after=payload.model_dump(exclude_unset=True),
    )
    db.commit()
    db.refresh(project)
    return project
