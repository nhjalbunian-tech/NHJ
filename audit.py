from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_permission
from app.models.audit import AuditLog
from app.models.user import User
from app.schemas.audit import AuditLogRead

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("", response_model=list[AuditLogRead])
def list_audit_logs(
    entity_type: str | None = None,
    entity_id: str | None = None,
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("audit:read")),
) -> list[AuditLog]:
    """Read-only by design — there is no PATCH/DELETE for audit entries anywhere in this API."""
    query = db.query(AuditLog)
    if entity_type:
        query = query.filter(AuditLog.entity_type == entity_type)
    if entity_id:
        query = query.filter(AuditLog.entity_id == entity_id)
    return query.order_by(AuditLog.timestamp.desc()).all()
