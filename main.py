from fastapi import FastAPI
from app.routers import users, tasks, auth

app = FastAPI()

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "API is running"}