from fastapi import FastAPI

from python_api.database import Base, engine
from python_api.routers import todos

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(todos.router)

@app.get("/health")
def root():
    return {"message": "health checked"}