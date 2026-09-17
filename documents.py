from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_permission
from app.models.document import ProjectDocument
from app.models.user import User
from app.schemas.document import DocumentCreate, DocumentRead
from app.services import audit_service

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
def create_document(
    payload: DocumentCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("document:create")),
) -> ProjectDocument:
    doc = ProjectDocument(**payload.model_dump(), uploaded_by_id=user.id)
    db.add(doc)
    db.flush()
    audit_service.record(
        db, entity_type="project_document", entity_id=doc.id, action="create",
        actor_id=user.id, after=payload.model_dump(),
    )
    db.commit()
    db.refresh(doc)
    return doc


@router.get("", response_model=list[DocumentRead])
def list_documents(
    project_id: str,
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("document:read")),
) -> list[ProjectDocument]:
    return db.query(ProjectDocument).filter(ProjectDocument.project_id == project_id).all()
