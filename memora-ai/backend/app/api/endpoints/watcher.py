from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
import os
from typing import Any

from app.api import deps
from app.models.user import User
from app.services.watcher import watcher_instance

router = APIRouter()

class WatcherConfig(BaseModel):
    workspace_path: str

@router.post("/start")
def start_watcher(
    config: WatcherConfig,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    if not os.path.isdir(config.workspace_path):
        raise HTTPException(status_code=400, detail="Invalid workspace path")
        
    watcher_instance.start(config.workspace_path)
    return {"status": "watching", "path": config.workspace_path}

@router.post("/stop")
def stop_watcher(
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    watcher_instance.stop()
    return {"status": "stopped"}

@router.get("/status")
def watcher_status(
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    is_running = watcher_instance.observer is not None and watcher_instance.observer.is_alive()
    return {
        "is_running": is_running
    }
