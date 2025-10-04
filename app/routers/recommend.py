from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.services.recommender import RecommenderService
from app.models import Hostel
from app.tasks.recommender import train_recommender

router = APIRouter()
recommender = RecommenderService()


# @router.post("/train")
# def train(session: Session = Depends(get_session)):
#     ok = recommender.train(session)
#     return {"trained": ok}
@router.post("/train")
def trigger_training():
    task = train_recommender.delay()  # async call
    return {"task_id": task.id, "status": "queued"}


@router.get("/for-student/{student_id}")
def recommend_for_student(student_id: int, session: Session = Depends(get_session)):
    hostel_ids = recommender.recommend(student_id, session)
    if not hostel_ids:
        return {"message": "No recommendations yet"}
    results = session.exec(Hostel).all()
    filtered = [h.dict() for h in results if h.id in hostel_ids]
    return {"recommendations": filtered}
