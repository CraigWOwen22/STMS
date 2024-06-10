from pydantic import BaseModel

class UserResp(BaseModel):
    username: str
    password: str

    class Config():
        orm_mode = True


class BookingResp(BaseModel):
    section: str
    show: str
    seats: int
    bookingDate: str

    

    class Config():
        orm_mode = True



class TheatreResp(BaseModel):
    section:str
    seats: int
    prices: int
    

    class Config():
        orm_mode = True


    