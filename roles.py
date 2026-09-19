from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_permission
from app.models.user import Role, User
from app.schemas.user import RoleRead

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("", response_model=list[RoleRead], dependencies=[Depends(require_permission("*"))])
def list_roles(db: Session = Depends(get_db)) -> list[Role]:
    """Admin-only, same as the user list — needed so the Users/Roles UI can populate a role picker."""
    return db.query(Role).order_by(Role.name).all()
