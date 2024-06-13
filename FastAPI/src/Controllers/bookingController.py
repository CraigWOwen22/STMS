from datetime import date
from ..database import get_db
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import services
from ..schemas import  BookingResp, BookingCreate



router = APIRouter(prefix="/bookings")


@router.post("/create", response_model=BookingResp, tags=["bookings"])
def create( bookingData: BookingCreate, db: Session = Depends(get_db), token = Depends(services.decryptAccessToken)):
    userID = token["userID"]
    bookingData = {'price': bookingData.price, 'seats': bookingData.seats, 'section': bookingData.section, 'bookingDate': bookingData.bookingDate}
    booking = services.createBooking(db, bookingData, userID)
    return booking

@router.get("/getall", response_model=list[BookingResp], tags=["bookings"])
def getAll( db: Session = Depends(get_db), token = Depends(services.decryptAccessToken)):
    userID = token["userID"]
    bookings = services.getAllBookings(db, userID)
    return bookings

@router.get("/getallsectionseats", tags=["bookings"])
def getAllSectionSeats(dateData: date, db: Session = Depends(get_db)):
    count = services.getAllSectionSeats(dateData, db)
    return count

@router.get("/getAllSeats", tags=["bookings"])
def getAllSeats(dateData: date, db: Session = Depends(get_db)):
    count = services.getAllSeats(dateData, db)
    return count

@router.delete("/{booking_id}", tags=["bookings"])
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = services.deleteBookingByID(booking_id, db)
    return booking
   


    