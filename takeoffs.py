from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_permission
from app.models.takeoff import EngineerTakeoff
from app.models.user import User
from app.schemas.takeoff import EngineerTakeoffCreate, EngineerTakeoffRead, ReviseTakeoffRequest, RevisionRead
from app.services import takeoff_service

router = APIRouter(prefix="/engineer-takeoffs", tags=["engineer-takeoffs"])


def _get_or_404(db: Session, takeoff_id: str) -> EngineerTakeoff:
    takeoff = db.get(EngineerTakeoff, takeoff_id)
    if not takeoff:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Takeoff not found")
    return takeoff


@router.post("", response_model=EngineerTakeoffRead, status_code=status.HTTP_201_CREATED)
def create_takeoff(
    payload: EngineerTakeoffCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("takeoff:create")),
) -> EngineerTakeoff:
    return takeoff_service.create_takeoff(
        db,
        project_id=payload.project_id,
        discipline=payload.discipline,
        title=payload.title,
        lines=payload.lines,
        user_id=user.id,
    )


@router.get("/{takeoff_id}", response_model=EngineerTakeoffRead)
def get_takeoff(
    takeoff_id: str, db: Session = Depends(get_db), _user: User = Depends(require_permission("takeoff:read"))
) -> EngineerTakeoff:
    return _get_or_404(db, takeoff_id)


@router.post("/{takeoff_id}/lock", response_model=RevisionRead)
def lock_current_revision(
    takeoff_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("takeoff:lock")),
) -> RevisionRead:
    takeoff = _get_or_404(db, takeoff_id)
    return takeoff_service.lock_revision(db, takeoff=takeoff, user_id=user.id)


@router.post("/{takeoff_id}/revise", response_model=RevisionRead, status_code=status.HTTP_201_CREATED)
def create_new_revision(
    takeoff_id: str,
    payload: ReviseTakeoffRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("takeoff:update")),
) -> RevisionRead:
    takeoff = _get_or_404(db, takeoff_id)
    return takeoff_service.create_revision(
        db, takeoff=takeoff, lines=payload.lines, notes=payload.notes, user_id=user.id
    )
