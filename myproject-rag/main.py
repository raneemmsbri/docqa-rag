from fastapi import FastAPI
from routes.qa import qa_router
from config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="نظام Document Q&A مبني بـ FastAPI + LangChain",
)

app.include_router(qa_router)


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }
