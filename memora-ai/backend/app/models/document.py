from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.db.base import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_type = Column(String)  # pdf, docx, md, etc
    project_id = Column(Integer, ForeignKey("projects.id"))
    module = Column(String)
    tags = Column(String)
    uploader_id = Column(Integer, ForeignKey("users.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    knowledge_entry_id = Column(Integer, ForeignKey("knowledge_entries.id"), nullable=True)
    
    content = Column(Text, nullable=False)
    embedding = Column(Vector(768)) # Using bge-base-en-v1.5 which has 768 dims (or OpenAI which has 1536, adjust as needed)
    
    # Metadata for filtering
    project_id = Column(Integer, ForeignKey("projects.id"))
