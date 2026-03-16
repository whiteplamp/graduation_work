from fastapi import APIRouter, HTTPException, status
from peewee import DoesNotExist

from src.core.db import database
from src.core.security import create_access_token, get_password_hash, verify_password
from src.models import User
from src.schemas import LoginRequest, Token, UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


def authenticate_user(_login: str, password: str) -> User | None:
    try:
        user = User.get(User.email == _login)
    except DoesNotExist:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


@router.post("/register", response_model=Token)
def register(data: UserCreate):
    with database.atomic():
        if User.select().where(User.email == data.email).exists():
            raise HTTPException(status_code=400, detail="User with this email already exists")
        user = User.create(
            name=data.name,
            email=data.email,
            hashed_password=get_password_hash(data.password),
        )
        token = create_access_token(str(user.id))
        return Token(token=token, user=UserOut.model_validate(user))


@router.post("/login", response_model=Token)
def login(body: LoginRequest):
    with database.connection_context():
        user = authenticate_user(body.login, body.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect login or password",
            )
        token = create_access_token(str(user.id))
        return Token(token=token, user=UserOut.model_validate(user))


