
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String) 

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    userID = Column(Integer, ForeignKey("users.id"))
    section = Column(String(1))
    show = Column(String(50))
    seats = Column(Integer)
    totalPrice = Column(Integer)
    bookingDate = Column(String(10)) 

class Theatre(Base):
    __tablename__ = "theatre"

    id = Column(Integer, primary_key=True, index=True)
    section = Column(String(1))
    seats = Column(Integer)

    
