from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_permission
from app.models.approval import ApprovalRequest
from app.models.user import User
from app.schemas.approval import ApprovalActionRequest, ApprovalRequestCreate, ApprovalRequestRead
from app.services import approval_service

router = APIRouter(prefix="/approvals", tags=["approvals"])


@router.post("", response_model=ApprovalRequestRead, status_code=status.HTTP_201_CREATED)
def create_approval_request(
    payload: ApprovalRequestCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("approval:act")),
) -> ApprovalRequest:
    steps = [s.model_dump() for s in payload.steps]
    return approval_service.create_request(
        db, entity_type=payload.entity_type, entity_id=payload.entity_id, steps=steps, requested_by_id=user.id
    )


@router.get("/{request_id}", response_model=ApprovalRequestRead)
def get_approval_request(
    request_id: str,
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("approval:act")),
) -> ApprovalRequest:
    request = db.get(ApprovalRequest, request_id)
    if not request:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Approval request not found")
    return request


@router.post("/{request_id}/act", response_model=ApprovalRequestRead)
def act_on_approval(
    request_id: str,
    payload: ApprovalActionRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("approval:act")),
) -> ApprovalRequest:
    request = db.get(ApprovalRequest, request_id)
    if not request:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Approval request not found")
    return approval_service.act_on_step(
        db, request=request, approve=payload.approve, comments=payload.comments, actor_id=user.id
    )
