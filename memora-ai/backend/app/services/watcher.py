import os
import time
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.document import Document, DocumentChunk
from app.services.rag import get_embeddings, process_text_into_chunks

class ProjectMemoryHandler(FileSystemEventHandler):
    def __init__(self, workspace_path: str):
        self.workspace_path = workspace_path
        # Use a new DB session for background thread
        self.db = SessionLocal()

    def _process_file(self, event):
        if event.is_directory:
            return
        
        file_path = event.src_path
        # Ignore common non-source directories/files
        if any(ignored in file_path for ignored in ['.git', 'node_modules', '__pycache__', '.venv', 'venv']):
            return
        if not (file_path.endswith('.py') or file_path.endswith('.tsx') or file_path.endswith('.ts') or file_path.endswith('.js') or file_path.endswith('.md')):
            return

        print(f"Memory Logger: Detected change in {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple chunking and embedding
            chunks = process_text_into_chunks(content)
            if not chunks:
                return

            embedder = get_embeddings()
            embeddings = embedder.embed_documents(chunks)
            
            filename = os.path.relpath(file_path, self.workspace_path)
            
            # Upsert document
            doc = self.db.query(Document).filter(Document.filename == filename).first()
            if not doc:
                doc = Document(filename=filename, file_type=filename.split('.')[-1])
                self.db.add(doc)
                self.db.commit()
                self.db.refresh(doc)
            else:
                # Delete old chunks for this document
                self.db.query(DocumentChunk).filter(DocumentChunk.document_id == doc.id).delete()
                self.db.commit()
                
            # Add new chunks
            for chunk_text, embedding in zip(chunks, embeddings):
                db_chunk = DocumentChunk(
                    document_id=doc.id,
                    content=chunk_text,
                    embedding=embedding
                )
                self.db.add(db_chunk)
            self.db.commit()
            print(f"Memory Logger: Ingested {len(chunks)} chunks for {filename}")

        except Exception as e:
            print(f"Memory Logger: Error processing {file_path} - {e}")
            self.db.rollback()

    def on_modified(self, event):
        self._process_file(event)
        
    def on_created(self, event):
        self._process_file(event)

class MemoryWatcher:
    def __init__(self):
        self.observer = None
        self.thread = None

    def start(self, path: str):
        if self.observer:
            self.stop()
            
        print(f"Starting Sidecar Memory Watcher on: {path}")
        event_handler = ProjectMemoryHandler(path)
        self.observer = Observer()
        self.observer.schedule(event_handler, path, recursive=True)
        self.observer.start()

    def stop(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None

watcher_instance = MemoryWatcher()
