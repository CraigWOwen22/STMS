from pydantic import BaseModel
from datetime import date

class UserResp(BaseModel):
    username: str
    password: str

    class Config():
        orm_mode = True


class BookingResp(BaseModel):
    id: int 
    section: str
    seats: int
    price: float
    bookingDate: date

    

    class Config():
        orm_mode = True

class BookingCreate(BaseModel):
    section: str
    seats: int
    price: float #Change to float?
    bookingDate: date



class TheatreResp(BaseModel):
    section:str
    seats: int
    prices: int
    

    class Config():
        orm_mode = True


    