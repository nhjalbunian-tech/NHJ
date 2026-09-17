from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_permission
from app.models.takeoff import AITakeoff, EngineerTakeoffRevision
from app.models.user import User
from app.models.verify import VerificationLine, VerificationSession
from app.schemas.verify import (
    SubmitVerifierQtyRequest,
    VerificationLineBlindRead,
    VerificationLineFullRead,
    VerificationSessionCreate,
    VerificationSessionRead,
)
from app.services import verify_service

router = APIRouter(prefix="/verify", tags=["verify"])


@router.post("/sessions", response_model=VerificationSessionRead, status_code=status.HTTP_201_CREATED)
def create_session(
    payload: VerificationSessionCreate,
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("verify:create")),
) -> VerificationSession:
    revision = db.get(EngineerTakeoffRevision, payload.engineer_revision_id)
    ai_takeoff = db.get(AITakeoff, payload.ai_takeoff_id)
    if not revision or not ai_takeoff:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Engineer revision or AI takeoff not found")
    if not revision.is_locked:
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Engineer revision must be locked before verification"
        )

    return verify_service.start_session(
        db,
        project_id=payload.project_id,
        engineer_revision=revision,
        ai_takeoff=ai_takeoff,
        verifier_id=payload.verifier_id,
    )


@router.get("/sessions/{session_id}/lines", response_model=list[VerificationLineBlindRead])
def list_blind_lines(
    session_id: str,
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("verify:read")),
) -> list[VerificationLine]:
    """Returns lines WITHOUT engineer/AI quantities — the blind view."""
    session = db.get(VerificationSession, session_id)
    if not session:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Verification session not found")
    return session.lines


@router.post("/lines/{line_id}/submit", response_model=VerificationLineFullRead)
def submit_verifier_quantity(
    line_id: str,
    payload: SubmitVerifierQtyRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("verify:update")),
) -> VerificationLine:
    """Submitting reveals engineer_qty/ai_qty and the computed variance for this line only."""
    line = db.get(VerificationLine, line_id)
    if not line:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Verification line not found")
    return verify_service.submit_verifier_qty(db, line=line, verifier_qty=payload.verifier_qty, actor_id=user.id)
