from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routes import router


BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="FitBuddy AI",
    description="AI-powered personalized fitness coach",
    version="1.0.0",
)

# Static files
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)

# IMPORTANT: include routes
app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok", "message": "FitBuddy AI is running"}