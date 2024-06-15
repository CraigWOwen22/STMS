from datetime import date
from ..database import get_db
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import services
from ..schemas import  BookingResp, BookingCreate



router = APIRouter(prefix="/bookings")

#API to allow a booking to be added (TEST DONE)
@router.post("/create", response_model=BookingResp, tags=["bookings"])
def create( bookingData: BookingCreate, db: Session = Depends(get_db), token = Depends(services.decryptAccessToken)):
    userID = token["userID"]
    bookingData = {'price': bookingData.price, 'seats': bookingData.seats, 'section': bookingData.section, 'bookingDate': bookingData.bookingDate}
    booking = services.createBooking(db, bookingData, userID)
    return booking

#API to get all the bookings releated to the user ID
@router.get("/getall", response_model=list[BookingResp], tags=["bookings"])
def getAll( db: Session = Depends(get_db), token = Depends(services.decryptAccessToken)):
    userID = token["userID"]
    bookings = services.getAllBookings(db, userID)
    return bookings

#API to get all seats remaining based on given date (TEST DONE)
@router.get("/getallsectionseats", tags=["bookings"])
def getAllSectionSeats(dateData: date, db: Session = Depends(get_db)):
    count = services.getAllSectionSeats(dateData, db)
    return count

#API to get total seats in theatre based on given date
@router.get("/getallseats", tags=["bookings"])
def getAllSeats(dateData: date, db: Session = Depends(get_db)):
    count = services.getAllSeats(dateData, db)
    return count

#API to remove a booking from the bookings
@router.delete("/{booking_id}", tags=["bookings"])
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = services.deleteBookingByID(booking_id, db)
    return booking
   


    