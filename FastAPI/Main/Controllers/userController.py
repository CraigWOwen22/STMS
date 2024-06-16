from ..database import get_db
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import services, schemas
from ..schemas import UserResp, UserCreate


router = APIRouter(prefix="/users")

# API to create a new user (Admin use only)
@router.post("/create", tags=["users"])
def create( userData: UserCreate, db: Session = Depends(get_db)):
    userData = {'username': userData.username, 'password': userData.password}
    user = services.createUser(db, userData)
    return user

# API to get all current users (Admin use only)
@router.get("/getall", response_model=list[UserResp], tags=["users"])
def getAll(db: Session = Depends(get_db)):
    users = services.getAllUsers(db)
    return users


    