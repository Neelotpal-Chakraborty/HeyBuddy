from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.rag_service import RAGService
from pydantic import BaseModel

router = APIRouter()


class RAGQuery(BaseModel):
    user_id: int
    question: str
    top_k: int = 5


@router.post('/index/{user_id}')
def index_user(user_id: int, db: Session = Depends(get_db)):
    """Index all diary entries for a user (compute embeddings)."""
    count = RAGService.index_user_diaries(db, user_id)
    return {'indexed': count}


@router.post('/chat')
def rag_chat(payload: RAGQuery, db: Session = Depends(get_db)):
    """Query user's diary entries with RAG and return assistant answer and sources"""
    answer, contexts = RAGService.query_user_diaries(db, payload.user_id, payload.question, payload.top_k)
    return {'answer': answer, 'contexts': contexts}
