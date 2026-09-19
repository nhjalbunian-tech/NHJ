from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_permission
from app.core.security import hash_password, validate_password_strength
from app.models.user import Role, User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services import audit_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.get("", response_model=list[UserRead], dependencies=[Depends(require_permission("*"))])
def list_users(db: Session = Depends(get_db)) -> list[User]:
    return db.query(User).all()


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("*")),
) -> User:
    """
    Admin-only user creation with a chosen role — this is the proper way
    to create a privileged account. (Public self-signup at /auth/register
    always gets the fixed low-privilege default role instead.)
    """
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already registered")

    role = db.query(Role).filter(Role.name == payload.role_name).first()
    if role is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Unknown role: {payload.role_name}")

    error = validate_password_strength(payload.password)
    if error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, error)

    username = (payload.username or payload.email.split("@")[0]).strip().lower()
    if not username or db.query(User).filter(User.username == username).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "اسم المستخدم مستخدم بالفعل")

    user = User(
        username=username,
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
        must_change_password=True,
        role_id=role.id,
    )
    db.add(user)
    db.flush()
    audit_service.record(
        db, entity_type="user", entity_id=user.id, action="create",
        actor_id=admin.id, after={"email": payload.email, "role_name": payload.role_name},
    )
    db.commit()
    db.refresh(user)
    return user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: str,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission("*")),
) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    before = {"role_id": user.role_id, "is_active": user.is_active}
    data = payload.model_dump(exclude_unset=True)

    if "role_id" in data:
        if not db.get(Role, data["role_id"]):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Unknown role_id")
        user.role_id = data["role_id"]
    if "is_active" in data:
        if user.id == admin.id and data["is_active"] is False:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Cannot deactivate your own account")
        user.is_active = data["is_active"]

    audit_service.record(
        db, entity_type="user", entity_id=user.id, action="update",
        actor_id=admin.id, before=before, after=data,
    )
    db.commit()
    db.refresh(user)
    return user
