from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DocumentBase(BaseModel):
    filename: str
    file_type: Optional[str] = None
    project_id: Optional[int] = None
    module: Optional[str] = None
    tags: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentInDB(DocumentBase):
    id: int
    uploader_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class SearchQuery(BaseModel):
    query: str
    project_id: Optional[int] = None
    module: Optional[str] = None
    limit: int = 5

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    project_id: Optional[int] = None
