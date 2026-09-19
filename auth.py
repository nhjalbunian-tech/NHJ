from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.security import create_access_token, hash_password, validate_password_strength, verify_password
from app.models.user import Role, User
from app.schemas.user import ChangePasswordRequest, Token, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    """
    Public self-signup. Deliberately ignores payload.role_name — without
    auth, letting the caller choose their own role (including "admin")
    would be an open privilege-escalation hole. Every self-registered
    account gets the fixed low-privilege default below; an admin must
    promote it afterwards via PATCH /users/{id} or create privileged
    accounts directly via POST /users.
    """
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already registered")

    default_role = db.query(Role).filter(Role.name == "engineer").first()

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
        role_id=default_role.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    login_name = form_data.username.strip().lower()
    user = db.query(User).filter(User.username == login_name).first()
    if user is None:
        user = db.query(User).filter(User.email == login_name).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(subject=user.id, extra_claims={"role": user.role.name})
    return Token(access_token=token, must_change_password=user.must_change_password)


@router.post("/change-password", response_model=UserRead)
def change_password(
    payload: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    error = validate_password_strength(payload.new_password)
    if error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, error)
    if not verify_password(payload.current_password, current_user.hashed_password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "كلمة المرور الحالية غير صحيحة")
    if verify_password(payload.new_password, current_user.hashed_password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "يجب اختيار كلمة مرور جديدة")
    current_user.hashed_password = hash_password(payload.new_password)
    current_user.must_change_password = False
    db.commit()
    db.refresh(current_user)
    return current_user
