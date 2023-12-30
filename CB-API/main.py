from fastapi import FastAPI
from database import engine
from Routers import birthday, auth
import models as m
import uvicorn

app = FastAPI()
m.Base.metadata.create_all(bind=engine)
app.include_router(birthday.router)
app.include_router(auth.router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8080)
