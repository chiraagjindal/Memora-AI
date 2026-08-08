from pydantic import BaseModel
from typing import Optional, List

class KnowledgeEntryBase(BaseModel):
    title: str
    project_id: Optional[int] = None
    module: Optional[str] = None
    category: Optional[str] = None
    
    description: str
    problem_statement: Optional[str] = None
    root_cause: Optional[str] = None
    solution: str
    prevention: Optional[str] = None
    
    related_files: Optional[str] = None
    related_apis: Optional[str] = None
    dependencies: Optional[str] = None
    programming_language: Optional[str] = None
    framework: Optional[str] = None
    environment: Optional[str] = None
    tags: Optional[str] = None

class KnowledgeEntryCreate(KnowledgeEntryBase):
    pass

class KnowledgeEntryUpdate(KnowledgeEntryBase):
    title: Optional[str] = None
    description: Optional[str] = None
    solution: Optional[str] = None

class KnowledgeEntryInDB(KnowledgeEntryBase):
    id: int
    author_id: int
    reviewer_id: Optional[int] = None
    is_approved: bool

    class Config:
        from_attributes = True
