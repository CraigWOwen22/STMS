from .schemas import UserResp, BookingResp, TheatreResp
from .models import User, Booking, Theatre
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from fastapi import HTTPException


########## User Services ##########

#Create a user
def createUser(db: Session, userData: UserResp):



    user = User(username = userData['username'], password = userData['password'])
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


########## Booking Services ##########

#Create a booking
#Need to add functionality to only book if capacity allows
def createBooking(db: Session, bookingData: BookingResp):
    
    seatsRemainDict = getAllSectionSeats(bookingData['bookingDate'], db)

    for item in seatsRemainDict:
        if item['key'] == bookingData['section']:
            test = item['value']

    if bookingData['seats'] > test:
        raise HTTPException(status_code=409, detail=f"No seats left for section: {bookingData['section']}")
        
    booking = Booking(show = bookingData['show'], seats = bookingData['seats'], section = bookingData['section'], bookingDate = bookingData['bookingDate'])

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking


#Get all bookings
def getAllBookings(db:Session):

    return db.query(Booking).all()
    

#Get all users
def getAllUsers(db:Session):
    
    return db.query(User).all()


#Get remaining seats by section 
#Need to catch error when not all sections are present in DB
def getAllSectionSeats(dateData: str, db: Session):

    totalSeatsBySecRem = db.query(Booking.section,func.sum(Booking.seats)).filter(Booking.section.in_(['A', 'B', 'C']), Booking.bookingDate == dateData).group_by(Booking.section).all()
    totalSeatsBySec = db.query(Theatre.section,Theatre.seats).all()

    #print(totalSeatsBySecRem)
    #print(totalSeatsBySec)
    
    dict_totalSeatsBySecRem = dict(totalSeatsBySecRem)
    dict_totalSeatsBySec = dict(totalSeatsBySec)

    result_list = [{'key': key, 'value': dict_totalSeatsBySec[key] - dict_totalSeatsBySecRem[key]} for key in dict_totalSeatsBySec]

    return result_list


#Get total available seats
def getAllSeats(dateData: str, db:Session):

    totalSeatsBySecRem = db.query(Booking.section,func.sum(Booking.seats)).filter(Booking.section.in_(['A', 'B', 'C']), Booking.bookingDate == dateData).group_by(Booking.section).all()
    totalSeatsBySec = db.query(Theatre.section,Theatre.seats).all()

    dict_totalSeatsBySecRem = dict(totalSeatsBySecRem)
    dict_totalSeatsBySec = dict(totalSeatsBySec)

    result_list = [{'key': key, 'value': dict_totalSeatsBySec[key] - dict_totalSeatsBySecRem[key]} for key in dict_totalSeatsBySec]


    total_seats = sum(item['value'] for item in result_list)
    total_seats_dict = {'Total': total_seats}

    #print(total_seats_dict)
    
    return total_seats_dict
    

def deleteBookingByID(booking_id: int, db: Session): 
    
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    db.delete(booking)
    db.commit()
    
    return {"detail": "Booking deleted"}


   



  