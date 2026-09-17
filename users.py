from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_permission
from app.core.security import hash_password, validate_password_strength
from app.models.user import Role, User
from app.schemas.user import RoleRead, UserCreate, UserPasswordReset, UserRead, UserUpdate
from app.services import audit_service

router = APIRouter(prefix="/users", tags=["users"])


def _get_user_or_404(user_id: str, db: Session) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "المستخدم غير موجود")
    return user


def _get_role_or_404(role_name: str, db: Session) -> Role:
    role = db.query(Role).filter(Role.name == role_name).first()
    if role is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "الدور المحدد غير موجود")
    return role


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.get("/roles", response_model=list[RoleRead], dependencies=[Depends(require_permission("*"))])
def list_roles(db: Session = Depends(get_db)) -> list[Role]:
    return db.query(Role).order_by(Role.name).all()


@router.get("", response_model=list[UserRead], dependencies=[Depends(require_permission("*"))])
def list_users(db: Session = Depends(get_db)) -> list[User]:
    return db.query(User).order_by(User.created_at.desc()).all()


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    actor: User = Depends(require_permission("*")),
) -> User:
    username = (payload.username or payload.email.split("@")[0]).strip().lower()
    if not username:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "اسم المستخدم مطلوب")
    if db.query(User).filter((User.username == username) | (User.email == str(payload.email).lower())).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "اسم المستخدم أو البريد مستخدم بالفعل")
    password_error = validate_password_strength(payload.password)
    if password_error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, password_error)
    role = _get_role_or_404(payload.role_name, db)
    user = User(
        username=username,
        email=str(payload.email).lower(),
        full_name=payload.full_name.strip(),
        hashed_password=hash_password(payload.password),
        must_change_password=True,
        role_id=role.id,
    )
    db.add(user)
    db.flush()
    audit_service.record(db, entity_type="user", entity_id=user.id, action="create", actor_id=actor.id, after={"username": username, "role": role.name})
    db.commit()
    db.refresh(user)
    return user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: str,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    actor: User = Depends(require_permission("*")),
) -> User:
    user = _get_user_or_404(user_id, db)
    changes = payload.model_dump(exclude_unset=True)
    if "username" in changes and changes["username"]:
        changes["username"] = changes["username"].strip().lower()
    if "email" in changes and changes["email"]:
        changes["email"] = str(changes["email"]).lower()
    if "full_name" in changes and changes["full_name"]:
        changes["full_name"] = changes["full_name"].strip()
    if "role_name" in changes:
        role = _get_role_or_404(changes.pop("role_name"), db)
        changes["role_id"] = role.id
    for field in ("username", "email"):
        value = changes.get(field)
        if value and db.query(User).filter(getattr(User, field) == value, User.id != user.id).first():
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "اسم المستخدم أو البريد مستخدم بالفعل")
    if user.id == actor.id and changes.get("is_active") is False:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "لا يمكنك تعطيل حسابك الحالي")
    before = {"username": user.username, "email": user.email, "full_name": user.full_name, "is_active": user.is_active, "role_id": user.role_id}
    for field, value in changes.items():
        setattr(user, field, value)
    audit_service.record(db, entity_type="user", entity_id=user.id, action="update", actor_id=actor.id, before=before, after={k: v for k, v in changes.items() if k != "role_id"})
    db.commit()
    db.refresh(user)
    return user


@router.post("/{user_id}/reset-password", response_model=UserRead)
def reset_user_password(
    user_id: str,
    payload: UserPasswordReset,
    db: Session = Depends(get_db),
    actor: User = Depends(require_permission("*")),
) -> User:
    user = _get_user_or_404(user_id, db)
    password_error = validate_password_strength(payload.new_password)
    if password_error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, password_error)
    user.hashed_password = hash_password(payload.new_password)
    user.must_change_password = True
    audit_service.record(db, entity_type="user", entity_id=user.id, action="reset_password", actor_id=actor.id)
    db.commit()
    db.refresh(user)
    return user
