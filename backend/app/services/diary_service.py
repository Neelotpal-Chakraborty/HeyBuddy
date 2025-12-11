from sqlalchemy.orm import Session
from sqlalchemy import distinct
from app.models import Diary
from app.schemas import DiaryCreate, DiaryUpdate
from fastapi import HTTPException
from datetime import date


class DiaryService:
    """Service for diary entry operations"""

    @staticmethod
    def create_entry(db: Session, diary_data: DiaryCreate) -> Diary:
        # check if entry exists for user and date
        existing = (
            db.query(Diary)
            .filter(Diary.user_id == diary_data.user_id, Diary.date == diary_data.date)
            .first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="Diary entry for this date already exists")

        entry = Diary(user_id=diary_data.user_id, date=diary_data.date, content=diary_data.content)
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    @staticmethod
    def update_entry(db: Session, entry_id: int, diary_update: DiaryUpdate) -> Diary:
        entry = db.query(Diary).filter(Diary.id == entry_id).first()
        if not entry:
            raise HTTPException(status_code=404, detail="Diary entry not found")

        update_data = diary_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(entry, field, value)

        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    @staticmethod
    def get_entry_by_user_and_date(db: Session, user_id: int, entry_date: date) -> Diary:
        entry = (
            db.query(Diary)
            .filter(Diary.user_id == user_id, Diary.date == entry_date)
            .first()
        )
        if not entry:
            raise HTTPException(status_code=404, detail="Diary entry not found for the specified date")
        return entry

    @staticmethod
    def get_dates_for_user(db: Session, user_id: int) -> list[date]:
        rows = (
            db.query(distinct(Diary.date))
            .filter(Diary.user_id == user_id)
            .order_by(Diary.date.desc())
            .all()
        )
        # rows are tuples like (date,)
        return [r[0] for r in rows]