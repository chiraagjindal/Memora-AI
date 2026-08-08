from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.base import Base

class KnowledgeEntry(Base):
    __tablename__ = "knowledge_entries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    module = Column(String)
    category = Column(String)
    
    description = Column(Text)
    problem_statement = Column(Text)
    root_cause = Column(Text)
    solution = Column(Text)
    prevention = Column(Text)
    
    related_files = Column(Text)
    related_apis = Column(Text)
    dependencies = Column(Text)
    programming_language = Column(String)
    framework = Column(String)
    environment = Column(String)
    tags = Column(String) # Comma separated
    
    author_id = Column(Integer, ForeignKey("users.id"))
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    is_approved = Column(Boolean, default=False)
