from ..database import get_db
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import services
from ..schemas import  TheatreResp, TheatreCreate

router = APIRouter(prefix="/theatre")


#API to get all the prices per theatre section
@router.get("/getallprices", tags=["theatre"])
def getAll(db: Session = Depends(get_db)):
    data = services.getAllPrices(db)
    return [{"section": section, "price": price} for section, price in data]

#API to creat a new section in the theatre
@router.post("/createsection", response_model=TheatreResp, tags=["theatre"])
def create( sectionData: TheatreCreate, db: Session = Depends(get_db)):
    sectionData = {'section': sectionData.section, 'seats': sectionData.seats, 'prices': sectionData.prices}
    section = services.createSection(db, sectionData)
    return section