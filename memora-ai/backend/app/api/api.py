from fastapi import APIRouter
from app.api.endpoints import auth, knowledge, chat, watcher, telemetry

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(watcher.router, prefix="/watcher", tags=["watcher"])
api_router.include_router(telemetry.router, prefix="/telemetry", tags=["telemetry"])
