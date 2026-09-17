from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_permission
from app.models.takeoff import AITakeoff, AITakeoffLine
from app.models.user import User
from app.schemas.takeoff import AITakeoffCreate, AITakeoffRead
from app.services import audit_service

router = APIRouter(prefix="/ai-takeoffs", tags=["ai-takeoffs"])


@router.post("", response_model=AITakeoffRead, status_code=status.HTTP_201_CREATED)
def create_ai_takeoff(
    payload: AITakeoffCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("ai_takeoff:create")),
) -> AITakeoff:
    """
    Deliberately independent of any EngineerTakeoff — created from the same
    project documents but by the automated pipeline, so it can later be
    compared blind (see /verify) without either side seeing the other's
    numbers first.
    """
    ai_takeoff = AITakeoff(
        project_id=payload.project_id,
        discipline=payload.discipline,
        title=payload.title,
        model_version=payload.model_version,
    )
    db.add(ai_takeoff)
    db.flush()
    for line in payload.lines:
        db.add(AITakeoffLine(ai_takeoff_id=ai_takeoff.id, **line.model_dump()))

    audit_service.record(
        db, entity_type="ai_takeoff", entity_id=ai_takeoff.id, action="create",
        actor_id=user.id, after={"title": payload.title, "model_version": payload.model_version},
    )
    db.commit()
    db.refresh(ai_takeoff)
    return ai_takeoff


@router.get("/{ai_takeoff_id}", response_model=AITakeoffRead)
def get_ai_takeoff(
    ai_takeoff_id: str,
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("ai_takeoff:read")),
) -> AITakeoff:
    ai_takeoff = db.get(AITakeoff, ai_takeoff_id)
    if not ai_takeoff:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "AI takeoff not found")
    return ai_takeoff
