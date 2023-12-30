from datetime import timedelta, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from database import get_db
from sqlalchemy.orm import Session
from starlette import status

from jose import jwt, JWTError
import models as m

router = APIRouter(prefix="/auth", tags=["auth"])

db_dependency = Annotated[Session, Depends(get_db)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

SECRET_KEY = "794233b43da5ef389f73a956d687092e5f2a26eb83c3cb6ea7d84043b3a58cef"
ALGO = "HS256"


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(username: str, password: str, db):
    user = db.query(m.Users).filter(m.Users.username == username).first()
    authentication = bcrypt_context.verify(password, user.hashed_password)
    return user if user and authentication else False


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, ALGO)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if not username or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credantions",
            )
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credantions",
        )


@router.get("/")
async def get_all_users(db: db_dependency):
    return db.query(m.Users).all()


@router.post("/new_user")
async def create_new_user(db: db_dependency, new_user_request: CreateUserRequest):
    new_user = m.Users(
        username=new_user_request.username,
        email=new_user_request.email,
        first_name=new_user_request.first_name,
        last_name=new_user_request.last_name,
        hashed_password=bcrypt_context.hash(new_user_request.password),
        role=new_user_request.role,
    )
    db.add(new_user)
    db.commit()
    return new_user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credantions",
        )
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {"access_token": token, "token_type": "bearer"}
