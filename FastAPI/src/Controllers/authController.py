from fastapi import Depends, HTTPException, APIRouter
from ..schemas import UserResp
from sqlalchemy.orm import Session
from ..database import get_db
from .. import services

router = APIRouter(prefix="/authentication")

@router.post("/login", tags=["authentication"])
def login(userData: UserResp, db: Session = Depends(get_db)):
    userData = {'username': userData.username, 'password': userData.password}
    user = services.login(db, userData)
    return user