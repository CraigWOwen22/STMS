
from .database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship


#A table to store all users 
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String) 
    bookings = relationship("Booking", back_populates="user")

#A table to store current bookings with a relationship to users table to maintain data integrity 
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    userID = Column(Integer, ForeignKey("users.id"))
    section = Column(String(1))
    seats = Column(Integer)
    price = Column(Integer)
    bookingDate = Column(Date())
    user = relationship("User", back_populates="bookings")

#A table to store information on the theatre
class Theatre(Base):
    __tablename__ = "theatre"

    id = Column(Integer, primary_key=True, index=True)
    section = Column(String(1))
    seats = Column(Integer)
    prices = Column(Integer)

    
