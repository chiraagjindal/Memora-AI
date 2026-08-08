from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Any
import logging

# Assuming deps is implemented to yield db session
from app.api import deps
# Assuming RAG service exists
from app.services import rag

router = APIRouter()
logger = logging.getLogger(__name__)

class FileSaveEvent(BaseModel):
    file_path: str
    content: str
    timestamp: str

class TerminalEvent(BaseModel):
    name: str
    event: str
    timestamp: str

class GitCommitEvent(BaseModel):
    commit_hash: str
    message: str
    diff: str
    timestamp: str

@router.post("/file-save")
async def process_file_save(event: FileSaveEvent, db: Session = Depends(deps.get_db)) -> Any:
    """
    Ingest a file save event from the IDE.
    """
    logger.info(f"Received file save event for: {event.file_path}")
    # Here we would typically chunk the content and update the vector database
    # For now, we simulate processing using the rag service
    # rag.index_document(event.content, metadata={"source": event.file_path, "type": "file_save"})
    return {"status": "success", "message": f"Processed {event.file_path}"}

@router.post("/terminal-event")
async def process_terminal_event(event: TerminalEvent, db: Session = Depends(deps.get_db)) -> Any:
    """
    Ingest a terminal event from the IDE.
    """
    logger.info(f"Received terminal event: {event.name} - {event.event}")
    return {"status": "success"}

@router.post("/git-commit")
async def process_git_commit(event: GitCommitEvent, db: Session = Depends(deps.get_db)) -> Any:
    """
    Ingest a git commit event from the IDE.
    """
    logger.info(f"Received git commit: {event.commit_hash}")
    # rag.index_document(event.diff, metadata={"source": event.commit_hash, "type": "git_commit", "message": event.message})
    return {"status": "success"}
