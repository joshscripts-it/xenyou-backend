from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models import Hostel
from app.services.embeddings import EmbeddingService
from pydantic import BaseModel

router = APIRouter()
embedding_service = EmbeddingService()


class Query(BaseModel):
    text: str
    max_price: int | None = None


@router.post("/search")
def search(query: Query, session: Session = Depends(get_session)):
    # 1. Embed the query
    q_emb = embedding_service.embed(query.text)

    # 2. Search with pgvector (inner product)
    statement = (
        select(Hostel).order_by(Hostel.embedding.cosine_distance(q_emb)).limit(5)
    )
    results = session.exec(statement).all()

    # 3. Apply price filter
    if query.max_price:
        results = [r for r in results if r.price <= query.max_price]

    return {"results": [r.dict() for r in results]}
