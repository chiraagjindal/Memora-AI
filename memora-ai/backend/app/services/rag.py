import os
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.document import DocumentChunk
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

try:
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_core.messages import SystemMessage, HumanMessage
except ImportError:
    pass # Provide mock or require installation

def get_embeddings():
    if settings.OPENAI_API_KEY:
        return OpenAIEmbeddings(
            api_key=settings.OPENAI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            model="text-embedding-004"
        )
    # Fallback to a mock or open source embeddings if no key
    class MockEmbeddings:
        def embed_query(self, text): return [0.0] * 768
        def embed_documents(self, texts): return [[0.0] * 768 for _ in texts]
    return MockEmbeddings()

def get_llm():
    if settings.OPENAI_API_KEY:
        return ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            model="gemini-1.5-flash"
        )
    class MockLLM:
        def invoke(self, messages):
            class Response:
                content = "Mock LLM response. Missing API Key."
            return Response()
    return MockLLM()

def process_text_into_chunks(text_content: str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_text(text_content)
    return chunks

def search_similar_chunks(db: Session, query: str, limit: int = 5):
    embedder = get_embeddings()
    query_embedding = embedder.embed_query(query)
    
    query_embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

    sql_query = text("""
        SELECT id, document_id, knowledge_entry_id, content, 
               1 - (embedding <=> :embedding) AS similarity
        FROM document_chunks
        ORDER BY embedding <=> :embedding
        LIMIT :limit
    """)
    
    results = db.execute(sql_query, {"embedding": query_embedding_str, "limit": limit}).fetchall()
    
    return [
        {
            "id": r.id,
            "document_id": r.document_id,
            "knowledge_entry_id": r.knowledge_entry_id,
            "content": r.content,
            "similarity": r.similarity
        } for r in results
    ]

def ask_memora(db: Session, query: str) -> str:
    """
    Two-Tier RAG Policy Implementation:
    1. Retrieve project evidence from pgvector.
    2. If evidence exists, strictly use it and cite.
    3. If no evidence but it's a general SWE question, provide a "General Explanation".
    4. If it's project specific and no evidence, say "I don't know".
    """
    try:
        results = search_similar_chunks(db, query, limit=5)
    except Exception as e:
        logger.error(f"Error querying vector DB: {e}")
        results = []

    # High similarity threshold to ensure relevance
    relevant_chunks = [r for r in results if r['similarity'] > 0.75]
    
    llm = get_llm()

    if relevant_chunks:
        context = "\n\n".join([f"Source ID {r['id']}:\n{r['content']}" for r in relevant_chunks])
        sys_msg = SystemMessage(content=(
            "You are Memora AI, a strictly accurate Project Memory Engine. "
            "Answer the user's question ONLY using the provided Project Evidence. "
            "You MUST cite the Source ID for every claim. "
            "If the evidence does not contain the answer, say 'I don't know'."
            f"\n\nPROJECT EVIDENCE:\n{context}"
        ))
        response = llm.invoke([sys_msg, HumanMessage(content=query)])
        return response.content
    else:
        # Tier 2: Check if it's a general SWE question
        sys_msg = SystemMessage(content=(
            "You are Memora AI. The user asked a question, but there is NO project evidence available. "
            "If the question is a general software engineering or programming question, answer it and explicitly prepend your answer with '[General Explanation]'. "
            "If the question is specific to a project, feature, or code not provided, you MUST reply ONLY with: 'I don't know. No project evidence found.'"
        ))
        response = llm.invoke([sys_msg, HumanMessage(content=query)])
        return response.content
