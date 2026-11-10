from fastapi import FastAPI
from app.routers import router

app = FastAPI(title="Media Tracker API")

app.include_router(router)


@app.get("/")
def home():
    return {"message": "Media Tracker API"}


@app.get("/health")
def health():
    return {"status": "ok"}