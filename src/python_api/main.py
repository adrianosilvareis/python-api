from fastapi import FastAPI

from python_api.routers import todos

app = FastAPI()

app.include_router(todos.router)

@app.get("/health")
def root():
    return {"message": "health checked"}