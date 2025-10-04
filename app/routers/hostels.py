from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.models import Hostel
from app.services.embeddings import EmbeddingService

router = APIRouter()
embedding_service = EmbeddingService()


@router.post("/add")
def add_hostel(
    name: str, description: str, price: int, session: Session = Depends(get_session)
):
    emb = embedding_service.embed(description)
    hostel = Hostel(name=name, description=description, price=price, embedding=emb)
    session.add(hostel)
    session.commit()
    session.refresh(hostel)
    return {"message": "Hostel added", "id": hostel.id}
