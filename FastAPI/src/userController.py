from .database import get_db
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from . import services, schemas
from .schemas import UserResp


router = APIRouter(prefix="/users")


@router.post("/create")
# Switch below param around 
def create( userData: UserResp, db: Session = Depends(get_db)):
    userData = {'username': userData.username, 'password': userData.password}
    user = services.createUser(db, userData)
    return userData

@router.get("/getall", response_model=list[UserResp])
def getAll(db: Session = Depends(get_db)):
    users = services.getAllUsers(db)
    return users

    