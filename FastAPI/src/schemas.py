from pydantic import BaseModel

class UserResp(BaseModel):
    username: str
    password: str

    class Config():
        orm_mode = True


class BookingResp(BaseModel):
    section: str
    seat: int
    price: int
    userID: int

    

    class Config():
        orm_mode = True



class TheatreResp(BaseModel):
    section:str
    seats: int
    

    class Config():
        orm_mode = True


    