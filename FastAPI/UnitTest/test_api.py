from cgitb import text
from datetime import date
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from Main.database import Base, get_db
from Main.main import app
from Main.schemas import UserCreate
from Main.services import createUser, hashing  
from Main.models import User, Booking, Theatre  
from Main import hashing



DATABASE_URL = "sqlite://"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


############################################### Test 1 ###############################################

global_test_token = ""

def test_create_user():
    test_user_data = {
        "username": "CRAIG22",
        "password": "PASSWORD"
    }
    response = client.post("/users/create", json=test_user_data)
    assert response.status_code == 200  

    assert response.json()["username"] == test_user_data["username"]

    with TestingSessionLocal() as db:
        db_user = db.query(User).filter(User.username == test_user_data["username"]).first()
        assert db_user is not None  
        assert hashing.Hash.verify(test_user_data["password"], db_user.password) 


############################################### Test 2 ###############################################



def test_login_successful():

    global global_test_token

    with TestingSessionLocal() as db:
        test_user = User(username="testuser", password=hashing.Hash.bcrypt("testpassword"))
        db.add(test_user)
        db.commit()
        db.refresh(test_user)

    response = client.post("/authentication/login", json={"username": "testuser", "password": "testpassword"})

    assert response.status_code == 200

    assert "access_token" in response.json()

    global_test_token = response.json()["access_token"]
    print(f"Access Token: {global_test_token}")

############################################### Test 3 ###############################################


def test_login_incorrect_password():
    
    response = client.post("/authentication/login", json={"username": "testuser", "password": "wrongpassword"})
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Incorrect password"

############################################### Test 4 ###############################################


def test_login_user_not_found():

    response = client.post("/authentication/login", json={"username": "nonexistentuser", "password": "anypassword"})

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
    print(f"Access Token: {global_test_token}")


############################################### Test 5 ###############################################


@patch('Main.services.getAllSectionSeats')
def test_create_booking(mock_getAllSectionSeats):
    
    assert global_test_token, "Global test token should be set before creating a booking."

    mock_getAllSectionSeats.return_value = [
        {"key": "A", "value": 10},  
        {"key": "B", "value": 15},  
        {"key": "B", "value": 20}
    ]

    booking_data = {
        "price": 100.0,
        "seats": 2,
        "section": "A",
        "bookingDate": "2024-09-24"
    }

    response = client.post(
        "/bookings/create",
        json=booking_data,
        headers={"Authorization": f"Bearer {global_test_token}"}
    )

    assert response.status_code == 200

    booking_resp = response.json()
    assert "id" in booking_resp
    assert booking_resp["price"] == booking_data["price"]
    assert booking_resp["seats"] == booking_data["seats"]
    assert booking_resp["section"] == booking_data["section"]
    assert booking_resp["bookingDate"] == booking_data["bookingDate"]
    

############################################### Test 6 ###############################################


@patch('Main.services.getAllSectionSeats')
def test_get_all_section_seats(mock_getAllSectionSeats):
    mock_getAllSectionSeats.return_value = [
        {"key": "A", "value": 10},  
        {"key": "B", "value": 15},  
        {"key": "C", "value": 20} 
    ]

    test_date = "2024-09-22"
    headers = {"Content-Type": "application/json"}

    response = client.get(
        f"/bookings/getallsectionseats?dateData={test_date}",
        headers=headers
    )

    assert response.status_code == 200

    result = response.json()
    assert isinstance(result, list)

    assert len(result) == 3 
    assert result[0]["key"] == "A"
    assert result[0]["value"] == 10
    assert result[1]["key"] == "B"
    assert result[1]["value"] == 15
    assert result[2]["key"] == "C"
    assert result[2]["value"] == 20


############################################### Test 7 ###############################################


@patch('Main.services.getAllBookings')
@patch('Main.services.decryptAccessToken')
def test_get_all_bookings(mock_decryptAccessToken, mock_getAllBookings):
    global global_test_token

    with TestingSessionLocal() as db:
        test_user = User(username="bookinguser", password=hashing.Hash.bcrypt("bookingpassword"))
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        user_id = test_user.id

    mock_decryptAccessToken.return_value = {"userID": user_id}

    mock_getAllBookings.return_value = [
        {
            "id": 1,
            "price": 50.0,
            "seats": 2,
            "section": "A",
            "bookingDate": "2024-09-24"
        },
        {
            "id": 2,
            "price": 75.0,
            "seats": 3,
            "section": "B",
            "bookingDate": "2024-09-25"
        }
    ]

    response = client.get(
        "/bookings/getall",
        headers={"Authorization": f"Bearer {global_test_token}"}
    )

    assert response.status_code == 200

    bookings_resp = response.json()
    assert isinstance(bookings_resp, list)
    assert len(bookings_resp) == 2

    booking_resp1 = bookings_resp[0]
    booking_resp2 = bookings_resp[1]

    assert booking_resp1["id"] == 1
    assert booking_resp1["price"] == 50.0
    assert booking_resp1["seats"] == 2
    assert booking_resp1["section"] == "A"
    assert booking_resp1["bookingDate"] == "2024-09-24"

    assert booking_resp2["id"] == 2
    assert booking_resp2["price"] == 75.0
    assert booking_resp2["seats"] == 3
    assert booking_resp2["section"] == "B"
    assert booking_resp2["bookingDate"] == "2024-09-25"


 ############################################### Test 8 ###############################################


@patch('Main.services.getAllSeats')
def test_get_all_seats(mock_getAllSeats):
    mock_getAllSeats.return_value = {
        "A": 100,   
        "B": 150,   
        "C": 200    
    }

    with TestingSessionLocal() as db:
        section_data = [
            Theatre(section="A", seats=120),
            Theatre(section="B", seats=180),
            Theatre(section="C", seats=220)
        ]
        db.add_all(section_data)
        db.commit()

        booking_data = [
            Booking(section="A", seats=20, bookingDate=date(2024, 9, 24)),
            Booking(section="A", seats=30, bookingDate=date(2024, 9, 24)),
            Booking(section="B", seats=25, bookingDate=date(2024, 9, 24)),
            Booking(section="C", seats=50, bookingDate=date(2024, 9, 24))
        ]
        db.add_all(booking_data)
        db.commit()

    test_date = date(2024, 9, 24)
    response = client.get(f"/bookings/getallseats?dateData={test_date}")

    assert response.status_code == 200

    seats_resp = response.json()
    assert isinstance(seats_resp, dict)
    assert seats_resp["A"] == 100
    assert seats_resp["B"] == 150
    assert seats_resp["C"] == 200


############################################### Test 9 ###############################################


def test_delete_booking():
    with TestingSessionLocal() as db:
        booking_date = date(2024, 9, 24)
        example_booking = Booking(
            userID=1,  
            section="A",
            seats=2,
            price=20,  
            bookingDate=booking_date
        )
        db.add(example_booking)
        db.commit()

    booking_id = 1
    response = client.delete(f"/bookings/{booking_id}")

    assert response.status_code == 200

    with TestingSessionLocal() as db:
        deleted_booking = db.query(Booking).filter(Booking.id == booking_id).first()
        assert deleted_booking is None, "Booking was not deleted from the database"


############################################### Test 10 ###############################################


def test_get_all_users_with_password():
    with TestingSessionLocal() as db:
        password1_hashed = hashing.Hash.bcrypt("password1")
        password2_hashed = hashing.Hash.bcrypt("password2")
        user1 = User(username="user1", password=password1_hashed)
        user2 = User(username="user2", password=password2_hashed)
        db.add(user1)
        db.add(user2)
        db.commit()

    response = client.get("/users/getall")

    assert response.status_code == 200

    users_resp = response.json()
    assert isinstance(users_resp, list)
    assert len(users_resp) == 5 

    
    for user in users_resp:
        assert "username" in user
        assert "password" in user


############################################### Test 11 ###############################################



def test_get_all_prices():

    with TestingSessionLocal() as db:
        section_prices = [
            Theatre(section="A", prices=50.0),
            Theatre(section="B", prices=75.0),
            Theatre(section="C", prices=100.0)
        ]
        db.add_all(section_prices)
        db.commit()

    response = client.get("/theatre/getallprices")

    assert response.status_code == 200

    prices_resp = response.json()
    assert isinstance(prices_resp, list)
    assert len(prices_resp) == 6  

    expected_sections = {"A", "B", "C"}  
    for item in prices_resp:
        assert "section" in item
        assert "price" in item
        assert item["section"] in expected_sections


############################################### Test 12 ###############################################



def test_create_section():
    new_section_data = {
        "section": "D",
        "seats": 150,
        "prices": 120.0
    }

    response = client.post("/theatre/createsection", json=new_section_data)

    assert response.status_code == 200

    section_resp = response.json()
    assert section_resp["section"] == new_section_data["section"]
    assert section_resp["seats"] == new_section_data["seats"]
    assert section_resp["prices"] == new_section_data["prices"]

    with TestingSessionLocal() as db:
        section_in_db = db.query(Theatre).filter(Theatre.section == new_section_data["section"]).first()
        assert section_in_db is not None
        assert section_in_db.section == new_section_data["section"]
        assert section_in_db.seats == new_section_data["seats"]
        assert section_in_db.prices == new_section_data["prices"]
