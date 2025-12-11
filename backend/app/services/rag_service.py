import json
import math
from typing import List, Tuple
from app.models import Diary, DiaryVector
from sqlalchemy.orm import Session
from fastapi import HTTPException
from openai import OpenAI
import os

# Load sentence-transformers model for local embeddings (no API quota limits)
try:
    from sentence_transformers import SentenceTransformer
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    USE_LOCAL_EMBEDDINGS = True
except ImportError:
    embedder = None
    USE_LOCAL_EMBEDDINGS = False

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def embed_text(text: str) -> List[float]:
    if not USE_LOCAL_EMBEDDINGS or not embedder:
        raise HTTPException(status_code=500, detail='Embedding service not available. Install sentence-transformers: pip install sentence-transformers')
    try:
        emb = embedder.encode(text, convert_to_tensor=False)
        return emb.tolist() if hasattr(emb, 'tolist') else list(emb)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Embedding error: {str(e)}')


def cosine_similarity(a: List[float], b: List[float]) -> float:
    # simple cosine similarity
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class RAGService:
    @staticmethod
    def index_user_diaries(db: Session, user_id: int) -> int:
        """Compute embeddings for all diary entries for a user and store them."""
        entries = db.query(Diary).filter(Diary.user_id == user_id).all()
        if not entries:
            return 0
        count = 0
        for e in entries:
            # skip if vector already exists for diary_id
            exists = db.query(DiaryVector).filter(DiaryVector.diary_id == e.id).first()
            if exists:
                continue
            emb = embed_text(e.content)
            vec = DiaryVector(diary_id=e.id, user_id=e.user_id, embedding=json.dumps(emb))
            db.add(vec)
            count += 1
        db.commit()
        return count

    @staticmethod
    def ensure_index(db: Session, user_id: int):
        # create vectors if none exist
        existing = db.query(DiaryVector).filter(DiaryVector.user_id == user_id).first()
        if not existing:
            RAGService.index_user_diaries(db, user_id)

    @staticmethod
    def query_user_diaries(db: Session, user_id: int, question: str, top_k: int = 5) -> Tuple[str, List[dict]]:
        """Run a RAG query: find top_k similar diary entries and ask LLM to answer."""
        if not question:
            raise HTTPException(status_code=400, detail='Question is required')

        RAGService.ensure_index(db, user_id)

        vectors = db.query(DiaryVector).filter(DiaryVector.user_id == user_id).all()
        if not vectors:
            raise HTTPException(status_code=404, detail='No indexed diary vectors for user')

        q_emb = embed_text(question)
        scored = []
        for v in vectors:
            emb = json.loads(v.embedding)
            sim = cosine_similarity(q_emb, emb)
            scored.append((sim, v))
        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:top_k]

        # gather diary texts
        contexts = []
        for score, v in top:
            diary = db.query(Diary).filter(Diary.id == v.diary_id).first()
            if diary:
                contexts.append({'date': str(diary.date), 'content': diary.content, 'score': score})

        # Build prompt for LLM
        system = (
            "You are an assistant that answers user questions using only the provided diary entries. "
            "When relevant, reference the date of the diary entry. If you don't know, say you don't know."
        )

        context_texts = []
        for i, c in enumerate(contexts, start=1):
            context_texts.append(f"Entry {i} (date: {c['date']}):\n{c['content']}")

        prompt = (
            system + "\n\n" +
            "Here are the most relevant diary entries:\n" + "\n\n".join(context_texts) +
            "\n\nAnswer the following question based on the above entries:\n" + question + "\n\nProvide a concise helpful answer and mention the entry dates you relied on."
        )

        try:
            # use chat completions (OpenAI API for LLM response)
            if not client:
                raise HTTPException(status_code=500, detail='OpenAI API key not configured for LLM responses')
            resp = client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[{'role': 'system', 'content': system},
                          {'role': 'user', 'content': prompt}],
                max_tokens=512,
                temperature=0.2,
            )
            answer = resp.choices[0].message.content
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'LLM error: {str(e)}')

        return answer, contexts