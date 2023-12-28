from fastapi import FastAPI
import models as m
from database import engine, SessionLocal
import uvicorn

app = FastAPI()
m.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"root": "there is not shit here wtf dude chill"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
