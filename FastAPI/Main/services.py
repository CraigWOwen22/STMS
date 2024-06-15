from .schemas import UserResp, BookingResp, TheatreResp, UserCreate, BookingCreate
from .models import User, Booking, Theatre
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from fastapi import HTTPException, Depends
from . import hashing
import jwt
from fastapi.security import OAuth2PasswordBearer




########## Login Services ##########

SECRET_KEY = "Thomas"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def createAccessToken(userID):
    payload = {
        "userID": userID
        }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return token

def decryptAccessToken(token:str = Depends(oauth2_scheme)):
    try:

        decodedPayload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decodedPayload
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def login(db:Session, userData: User):
    user = db.query(User).filter(User.username == userData['username']).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    print(f"Username: {user.username}")
    print(f"Hashed Password: {user.password}")

    if not hashing.Hash.verify(userData['password'], user.password):
        raise HTTPException(status_code=404, detail="Incorrect password")
    
    token = createAccessToken(user.id)

    return {"access_token": token}



########## Theatre Services ##########

#create a new section in the theatre(dev)
def createSection(db: Session, sectionData: Theatre):

    existingSection = db.query(Theatre).filter(Theatre.section == sectionData['section']).first()
    if existingSection:
        raise HTTPException(status_code=400, detail="Section already exists")
    
    section = Theatre(section = sectionData['section'], seats = sectionData['seats'], prices = sectionData['prices'])
    db.add(section)
    db.commit()
    db.refresh(section)
    
    return section


#get all priced by section
def getAllPrices(db:Session):
    return db.query(Theatre.section, Theatre.prices).all()
    

########## User Services ##########

#create a new user(dev)
def createUser(db: Session, userData):
    if isinstance(userData, dict):
        userData = UserCreate(**userData)  # Convert dictionary to UserCreate instance

    existing_user = db.query(User).filter(User.username == userData.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_password = hashing.Hash.bcrypt(userData.password)  # Hash the password 
    
    user = User(username=userData.username, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user
    


########## Booking Services ##########

#create a new booking
def createBooking(db: Session, bookingData: BookingCreate, userID):
    
    seatsRemainDict = getAllSectionSeats(bookingData['bookingDate'], db) 
    
    for item in seatsRemainDict:
        if item['key'] == bookingData['section']: 
            test = item['value']  

    if bookingData['seats'] > test:
        raise HTTPException(status_code=409, detail=f"No seats left for section: {bookingData['section']}")

    booking = Booking(price = bookingData['price'], seats = bookingData['seats'], section = bookingData['section'], bookingDate = bookingData['bookingDate'], userID = userID)

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking


#get all current bookings related to token
def getAllBookings(db:Session, userID):

    return db.query(Booking).filter(Booking.userID == userID).all()

    

#get all current users (dev)
def getAllUsers(db:Session):
    
    return db.query(User).all()


#get remaining seats by section 
def getAllSectionSeats(dateData: str, db: Session):
    
    totalSeatsBySec = db.query(Theatre.section, Theatre.seats).all()
    
    sectionSeatsDict = dict(totalSeatsBySec)
    
    totalSeatsBookedBySec = db.query(Booking.section, func.sum(Booking.seats)).filter(
        Booking.section.in_(['A', 'B', 'C']),
        Booking.bookingDate == dateData).group_by(Booking.section).all()
    
    bookedSeatsDict = dict(totalSeatsBookedBySec)
    
    for section in ['A', 'B', 'C']:
        if section not in bookedSeatsDict:
            totalSeatsBookedBySec.append((section, 0))
        if section in sectionSeatsDict:
            bookedSeatsDict[section] = 0
        else:
            raise ValueError(f"Section '{section}' not found in the Theatre table.")

    dictTotalSeatsBySecRem = dict(totalSeatsBookedBySec)
    dictTotalSeatsBySec = dict(totalSeatsBySec)

    resultList = [{'key': key, 'value': dictTotalSeatsBySec[key] - dictTotalSeatsBySecRem[key]} 
               for key in dictTotalSeatsBySec 
               if key in dictTotalSeatsBySecRem]
    
    return resultList


#get total available seats
def getAllSeats(dateData: str, db:Session):

    #Futute improvement - Possibly the getAllSectionSeats can be used here to prevent repetitve code
     
    totalSeatsBySec = db.query(Theatre.section, Theatre.seats).all()
    
    sectionSeatsDict = dict(totalSeatsBySec)
    
    totalSeatsBookedBySec = db.query(Booking.section, func.sum(Booking.seats)).filter(
        Booking.section.in_(['A', 'B', 'C']),
        Booking.bookingDate == dateData).group_by(Booking.section).all()

   
    
    bookedSeatsDict = dict(totalSeatsBookedBySec)
    
    for section in ['A', 'B', 'C']:
        if section not in bookedSeatsDict:
            totalSeatsBookedBySec.append((section, 0))
        if section in sectionSeatsDict:
            bookedSeatsDict[section] = 0
        else:
            raise ValueError(f"Section '{section}' not found in the Theatre table.")

    dictTotalSeatsBySecRem = dict(totalSeatsBookedBySec)
    dictTotalSeatsBySec = dict(totalSeatsBySec)

    resultList = [{'key': key, 'value': dictTotalSeatsBySec[key] - dictTotalSeatsBySecRem[key]} 
               for key in dictTotalSeatsBySec
               if key in dictTotalSeatsBySecRem]

    total_seats = sum(item['value'] for item in resultList)
    totalSeatsDict = {'total': total_seats}

    return totalSeatsDict
    
#delete a booking by bookingid
def deleteBookingByID(booking_id: int, db: Session): 
    
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    db.delete(booking)
    db.commit()
    
    return {"detail": "Booking deleted"}


   



  