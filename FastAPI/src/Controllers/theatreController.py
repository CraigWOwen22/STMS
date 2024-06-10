from ..database import get_db
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import services
from ..schemas import  TheatreResp

router = APIRouter(prefix="/theatre")


@router.get("/getallPrices", tags=["theatre"])
def getAll(db: Session = Depends(get_db)):
    data = services.getAllPrices(db)
    return [{"section": section, "price": price} for section, price in data]

@router.post("/createsection", response_model=TheatreResp, tags=["theatre"])
def create( sectionData: TheatreResp, db: Session = Depends(get_db)):
    sectionData = {'section': sectionData.section, 'seats': sectionData.seats, 'prices': sectionData.prices}
    section = services.createSection(db, sectionData)
    return section