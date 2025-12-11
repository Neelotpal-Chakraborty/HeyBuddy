from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.diary_service import DiaryService
from app.schemas import DiaryCreate, DiaryUpdate, DiaryResponse, DiaryDatesResponse
from datetime import date
from fastapi import HTTPException

router = APIRouter()


@router.post("/", response_model=DiaryResponse, status_code=201)
def create_diary_entry(diary: DiaryCreate, db: Session = Depends(get_db)):
    """Create a diary entry for a user and date"""
    entry = DiaryService.create_entry(db, diary)
    return entry


@router.put("/{entry_id}", response_model=DiaryResponse)
def update_diary_entry(entry_id: int, diary_update: DiaryUpdate, db: Session = Depends(get_db)):
    """Update an existing diary entry by ID"""
    entry = DiaryService.update_entry(db, entry_id, diary_update)
    return entry


@router.get("/dates/{user_id}", response_model=DiaryDatesResponse)
def get_diary_dates(user_id: int, db: Session = Depends(get_db)):
    """Get all dates for which the user has diary entries"""
    dates = DiaryService.get_dates_for_user(db, user_id)
    return {"dates": dates}


@router.get("/{user_id}/{entry_date}", response_model=DiaryResponse)
def get_diary_by_date(user_id: int, entry_date: str, db: Session = Depends(get_db)):
    """Get diary content for a specific user and date. Date format: YYYY-MM-DD"""
    try:
        d = date.fromisoformat(entry_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    entry = DiaryService.get_entry_by_user_and_date(db, user_id, d)
    return entry
