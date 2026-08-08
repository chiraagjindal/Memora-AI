from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.models.knowledge import KnowledgeEntry
from app.schemas.knowledge import KnowledgeEntryCreate, KnowledgeEntryInDB, KnowledgeEntryUpdate

router = APIRouter()

@router.get("/", response_model=List[KnowledgeEntryInDB])
def read_knowledge_entries(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    entries = db.query(KnowledgeEntry).offset(skip).limit(limit).all()
    return entries

@router.post("/", response_model=KnowledgeEntryInDB)
def create_knowledge_entry(
    *,
    db: Session = Depends(deps.get_db),
    entry_in: KnowledgeEntryCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    entry = KnowledgeEntry(
        **entry_in.model_dump(),
        author_id=current_user.id,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    
    # TODO: Add background task to embed this entry and store in pgvector
    
    return entry

@router.get("/{id}", response_model=KnowledgeEntryInDB)
def read_knowledge_entry(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    entry = db.query(KnowledgeEntry).filter(KnowledgeEntry.id == id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Knowledge entry not found")
    return entry
