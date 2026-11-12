from fastapi import FastAPI
from app.routers import router
from app.auth import router as auth_router

app = FastAPI(title="Media Tracker API")

app.include_router(router)
app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "Media Tracker API"}


@app.get("/health")
def health():
    return {"status": "ok"}