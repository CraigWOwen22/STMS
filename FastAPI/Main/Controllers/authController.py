from fastapi import Depends, HTTPException, APIRouter
from ..schemas import UserCreate
from sqlalchemy.orm import Session
from ..database import get_db
from .. import services

router = APIRouter(prefix="/authentication")

# API to allow user to login to the system 
@router.post("/login", tags=["authentication"])
def login(userData: UserCreate, db: Session = Depends(get_db)):
    userData = {'username': userData.username, 'password': userData.password}
    user = services.login(db, userData)
    return user