from ..database import get_db
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import services
from ..schemas import UserResp, BookingResp, TheatreResp



router = APIRouter(prefix="/bookings")


@router.post("/create", response_model=BookingResp)
def create( bookingData: BookingResp, db: Session = Depends(get_db)):
    bookingData = {'show': bookingData.show, 'seats': bookingData.seats, 'section': bookingData.section, 'bookingDate': bookingData.bookingDate}
    booking = services.createBooking(db, bookingData)
    return booking

@router.get("/getall", response_model=list[BookingResp])
def getAll( db: Session = Depends(get_db)):
    bookings = services.getAllBookings(db)
    return bookings


@router.get("/getallsectionseats")
def getAllSectionSeats(dateData: str, db: Session = Depends(get_db)):
    count = services.getAllSectionSeats(dateData, db)
    return count

@router.get("/getAllSeats")
def getAllSeats(dateData: str, db: Session = Depends(get_db)):
    count = services.getAllSeats(dateData, db)
    return count


@router.delete("{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = services.deleteBookingByID(booking_id, db)
    return booking
   


    