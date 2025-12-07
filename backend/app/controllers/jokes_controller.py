from fastapi import APIRouter, Depends
from app.services.jokes_service import JokesService
from app.core.security import validate_access_token

router = APIRouter()

@router.get("/daily")
def get_daily_joke(user=Depends(validate_access_token)):
    return JokesService.get_daily_joke()
