# Interaction Logging Service → Track what students do (click, save, apply).
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.models import Interaction

router = APIRouter()


@router.post("/log")
def log_interaction(
    student_id: int,
    hostel_id: int,
    action: str,
    session: Session = Depends(get_session),
):
    interaction = Interaction(student_id=student_id, hostel_id=hostel_id, action=action)
    session.add(interaction)
    session.commit()
    return {"message": "Interaction logged"}
