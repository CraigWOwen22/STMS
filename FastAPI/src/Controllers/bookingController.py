from ..database import get_db
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import services
from ..schemas import  BookingResp



router = APIRouter(prefix="/bookings")


@router.post("/create", response_model=BookingResp, tags=["bookings"])
def create( bookingData: BookingResp, db: Session = Depends(get_db)):
    bookingData = {'show': bookingData.show, 'seats': bookingData.seats, 'section': bookingData.section, 'bookingDate': bookingData.bookingDate}
    booking = services.createBooking(db, bookingData)
    return booking

@router.get("/getall", response_model=list[BookingResp], tags=["bookings"])
def getAll( db: Session = Depends(get_db)):
    bookings = services.getAllBookings(db)
    return bookings


@router.get("/getallsectionseats", tags=["bookings"])
def getAllSectionSeats(dateData: str, db: Session = Depends(get_db)):
    count = services.getAllSectionSeats(dateData, db)
    return count

@router.get("/getAllSeats", tags=["bookings"])
def getAllSeats(dateData: str, db: Session = Depends(get_db)):
    count = services.getAllSeats(dateData, db)
    return count


@router.delete("{booking_id}", tags=["bookings"])
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = services.deleteBookingByID(booking_id, db)
    return booking
   


    