from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

#A class that provides functionality encrypt a password in the database and to verify the users password against it

class Hash():
    def bcrypt(password:str):
        return pwd_cxt.hash(password)

    def verify(plainPassword, hashedPassword):
        return pwd_cxt.verify(plainPassword, hashedPassword)