from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

router = APIRouter(prefix="/birthday", tags=["birthday"])


db_dependency = Annotated[Session, Depends(get_db)]


# Pydantic model
class BirthDayRequest(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = False


@router.get("/")
async def root():
    return {"root": "there is not shit here wtf dude chill"}
