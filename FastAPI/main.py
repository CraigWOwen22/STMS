from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Main.Controllers import userController, bookingController, theatreController, authController
from Main.database import Base, engine
from passlib.context import CryptContext

app = FastAPI()

origins = ["*"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])

app.include_router(userController.router)
app.include_router(bookingController.router)
app.include_router(theatreController.router)
app.include_router(authController.router)



Base.metadata.create_all(bind=engine)

