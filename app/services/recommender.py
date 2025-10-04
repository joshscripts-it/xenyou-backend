# Recommender Service (LightFM stub) → Train a hybrid (content + collaborative filtering) model.(Training is manually triggered for now)
import numpy as np
from lightfm import LightFM
from sqlmodel import Session, select
from app.models import Student, Hostel, Interaction
from app.database import get_session
from scipy.sparse import coo_matrix


class RecommenderService:
    def __init__(self):
        self.model = LightFM(loss="warp")

    def build_matrices(self, session: Session):
        students = session.exec(select(Student)).all()
        hostels = session.exec(select(Hostel)).all()
        interactions = session.exec(select(Interaction)).all()

        student_map = {s.id: i for i, s in enumerate(students)}
        hostel_map = {h.id: j for j, h in enumerate(hostels)}

        rows, cols, data = [], [], []
        for inter in interactions:
            if inter.student_id in student_map and inter.hostel_id in hostel_map:
                rows.append(student_map[inter.student_id])
                cols.append(hostel_map[inter.hostel_id])
                data.append(1.0 if inter.action in ["save", "apply"] else 0.5)

        mat = coo_matrix((data, (rows, cols)), shape=(len(students), len(hostels)))
        return mat, student_map, hostel_map

    def train(self, session: Session):
        interaction_matrix, student_map, hostel_map = self.build_matrices(session)
        if interaction_matrix.nnz > 0:
            self.model.fit(interaction_matrix, epochs=10, num_threads=2)
            return True
        return False

    def recommend(self, student_id: int, session: Session, top_n: int = 5):
        students = session.exec(select(Student)).all()
        hostels = session.exec(select(Hostel)).all()
        student_map = {s.id: i for i, s in enumerate(students)}
        hostel_map = {h.id: j for j, h in enumerate(hostels)}
        rev_hostel_map = {v: k for k, v in hostel_map.items()}

        if student_id not in student_map:
            return []

        scores = self.model.predict(student_map[student_id], np.arange(len(hostels)))
        top_items = np.argsort(-scores)[:top_n]
        return [rev_hostel_map[i] for i in top_items]
