from sqlmodel import SQLModel, Field
from typing import Optional, List
from pgvector.sqlalchemy import Vector


class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str


class Hostel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: int
    amenities: Optional[List[str]] = None
    # store embeddings directly in DB
    embedding: Optional[List[float]] = Field(sa_column=Vector(384))


# Add Interaction Logging:Track what students do (click, save, apply)
class Interaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    hostel_id: int = Field(foreign_key="hostel.id")
    action: str  # "view", "click", "save", "apply"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
