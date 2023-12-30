from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
import models as m

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


@router.get('/auth')
async def get_all_users(db:db_dependency):
    return db.query(m.Users).all()


@router.post('/auth/new_user')
async def create_new_user(db: db_dependency, new_user_request: CreateUserRequest):
    new_user = m.Users(
        username=new_user_request.username,
        email=new_user_request.email,
        first_name=new_user_request.first_name,
        last_name=new_user_request.last_name,
        hashed_password=new_user_request.password,
        role=new_user_request.role,
    )
    db.add(new_user)
    db.commit()
    return new_user
