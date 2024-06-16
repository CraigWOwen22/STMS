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
from Main.services import createUser, hashing  # Assuming createUser function and hashing is imported from services module
from Main.models import User, Booking, Theatre  # Assuming User model is imported from models module
from Main import hashing


# Define the in-memory SQLite database URL
DATABASE_URL = "sqlite://"

# Setup SQLAlchemy engine and session
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db function to use TestingSessionLocal
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Create tables in the in-memory database
Base.metadata.create_all(bind=engine)

# Override get_db dependency in app
app.dependency_overrides[get_db] = override_get_db

# Create TestClient instance
client = TestClient(app)


########################################################################################################

global_test_token = ""



# Example test case for POST /users/create endpoint
def test_create_user():
    # Define test data (replace with actual data as per your schema)
    test_user_data = {
        "username": "CRAIG22",
        "password": "PASSWORD"
    }

    # Make POST request to create user endpoint
    response = client.post("/users/create", json=test_user_data)

    # Assert the response status code
    assert response.status_code == 200  # Assuming createUser returns 200 OK on success

    # Assert the returned username matches the input
    assert response.json()["username"] == test_user_data["username"]

    # Retrieve the user from the database to check hashed password
    with TestingSessionLocal() as db:
        db_user = db.query(User).filter(User.username == test_user_data["username"]).first()
        assert db_user is not None  # Ensure user exists in the database
        assert hashing.Hash.verify(test_user_data["password"], db_user.password)  # Verify hashed password

    # Optionally, assert database state or perform additional checks

    ########################################################################################################

#create a login test that will create a token and store as global


# Example test cases for /authentication/login endpoint
def test_login_successful():

    global global_test_token

    # Create a user for testing
    with TestingSessionLocal() as db:
        test_user = User(username="testuser", password=hashing.Hash.bcrypt("testpassword"))
        db.add(test_user)
        db.commit()
        db.refresh(test_user)

    # Make a successful login request
    response = client.post("/authentication/login", json={"username": "testuser", "password": "testpassword"})

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response contains an access token
    assert "access_token" in response.json()

    global_test_token = response.json()["access_token"]
    print(f"Access Token: {global_test_token}")

def test_login_incorrect_password():
    # Make a login request with incorrect password
    response = client.post("/authentication/login", json={"username": "testuser", "password": "wrongpassword"})

    # Assert the response status code
    assert response.status_code == 404
    assert response.json()["detail"] == "Incorrect password"

def test_login_user_not_found():
    # Make a login request with non-existent username
    response = client.post("/authentication/login", json={"username": "nonexistentuser", "password": "anypassword"})

    # Assert the response status code
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
    print(f"Access Token: {global_test_token}")



########################################################################################################

@patch('Main.services.getAllSectionSeats')
def test_create_booking(mock_getAllSectionSeats):
    # Ensure global_test_token is set
    assert global_test_token, "Global test token should be set before creating a booking."

    mock_getAllSectionSeats.return_value = [
        {"key": "A", "value": 10},  
        {"key": "B", "value": 15},  
        {"key": "B", "value": 20}
    ]

    # Prepare booking data
    booking_data = {
        "price": 100.0,
        "seats": 2,
        "section": "A",
        "bookingDate": "2024-09-24"
    }

    # Make a booking creation request with the access token
    response = client.post(
        "/bookings/create",
        json=booking_data,
        headers={"Authorization": f"Bearer {global_test_token}"}
    )

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response contains the expected fields for booking response
    
    booking_resp = response.json()
    assert "id" in booking_resp
    assert booking_resp["price"] == booking_data["price"]
    assert booking_resp["seats"] == booking_data["seats"]
    assert booking_resp["section"] == booking_data["section"]
    assert booking_resp["bookingDate"] == booking_data["bookingDate"]
    


########################################################################################################

@patch('Main.services.getAllSectionSeats')
def test_get_all_section_seats(mock_getAllSectionSeats):
    # Mock the behavior of getAllSectionSeats
    mock_getAllSectionSeats.return_value = [
        {"key": "A", "value": 10},  
        {"key": "B", "value": 15},  
        {"key": "C", "value": 20} 
    ]

    # Prepare test data and request parameters
    test_date = "2024-09-22"
    headers = {"Content-Type": "application/json"}

    # Make a request to the endpoint
    response = client.get(
        f"/bookings/getallsectionseats?dateData={test_date}",
        headers=headers
    )

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response contains expected data structure
    result = response.json()
    assert isinstance(result, list)

    # Example specific assertions based on mocked data
    assert len(result) == 3 
    assert result[0]["key"] == "A"
    assert result[0]["value"] == 10
    assert result[1]["key"] == "B"
    assert result[1]["value"] == 15
    assert result[2]["key"] == "C"
    assert result[2]["value"] == 20




########################################################################################################


@patch('Main.services.getAllBookings')
@patch('Main.services.decryptAccessToken')
def test_get_all_bookings(mock_decryptAccessToken, mock_getAllBookings):
    global global_test_token

    # Create a test user
    with TestingSessionLocal() as db:
        test_user = User(username="bookinguser", password=hashing.Hash.bcrypt("bookingpassword"))
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        user_id = test_user.id

    # Mock the token decryption to return the test user's ID
    mock_decryptAccessToken.return_value = {"userID": user_id}

    # Mock the getAllBookings function to return a predefined list of bookings
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

    # Make a request to get all bookings
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

 ########################################################################################################

@patch('Main.services.getAllSeats')
def test_get_all_seats(mock_getAllSeats):
    # Mock the getAllSeats function to return a predefined count
    mock_getAllSeats.return_value = {
        "A": 100,   # Example total seats for section A
        "B": 150,   # Example total seats for section B
        "C": 200    # Example total seats for section C
    }

    # Example data setup in the database (optional for illustration)
    with TestingSessionLocal() as db:
        # Create example Theatre data
        section_data = [
            Theatre(section="A", seats=120),
            Theatre(section="B", seats=180),
            Theatre(section="C", seats=220)
        ]
        db.add_all(section_data)
        db.commit()

        # Create example Booking data
        booking_data = [
            Booking(section="A", seats=20, bookingDate=date(2024, 9, 24)),
            Booking(section="A", seats=30, bookingDate=date(2024, 9, 24)),
            Booking(section="B", seats=25, bookingDate=date(2024, 9, 24)),
            Booking(section="C", seats=50, bookingDate=date(2024, 9, 24))
        ]
        db.add_all(booking_data)
        db.commit()

    # Make a request to get all seats with a specific date
    test_date = date(2024, 9, 24)
    response = client.get(f"/bookings/getallseats?dateData={test_date}")

    # Assert the response status code
    assert response.status_code == 200

    # Assert the structure and content of the response
    seats_resp = response.json()
    assert isinstance(seats_resp, dict)
    assert seats_resp["A"] == 100
    assert seats_resp["B"] == 150
    assert seats_resp["C"] == 200




########################################################################################################

def test_delete_booking():
    # Example data setup in the database
    with TestingSessionLocal() as db:
        # Create an example booking
        booking_date = date(2024, 9, 24)
        example_booking = Booking(
            userID=1,  # Example userID
            section="A",
            seats=2,
            price=20,  # Example price
            bookingDate=booking_date
        )
        db.add(example_booking)
        db.commit()

    # Make a request to delete the booking with id=1
    booking_id = 1
    response = client.delete(f"/bookings/{booking_id}")

    # Assert the response status code
    assert response.status_code == 200

    # Verify that the booking was actually deleted from the database
    with TestingSessionLocal() as db:
        deleted_booking = db.query(Booking).filter(Booking.id == booking_id).first()
        assert deleted_booking is None, "Booking was not deleted from the database"

########################################################################################################

# Example test function
def test_get_all_users_with_password():
    # Insert mock users with hashed passwords
    with TestingSessionLocal() as db:
        password1_hashed = hashing.Hash.bcrypt("password1")
        password2_hashed = hashing.Hash.bcrypt("password2")
        user1 = User(username="user1", password=password1_hashed)
        user2 = User(username="user2", password=password2_hashed)
        db.add(user1)
        db.add(user2)
        db.commit()

    # Make a request to get all users
    response = client.get("/users/getall")

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response contains a list of users with username and hashed password
    users_resp = response.json()
    assert isinstance(users_resp, list)
    assert len(users_resp) == 5 #At this point in testing, 5 users exist 

    # Assert each user has username and password fields
    for user in users_resp:
        assert "username" in user
        assert "password" in user

########################################################################################################

def test_get_all_prices():
    # Insert mock theatre section prices
    with TestingSessionLocal() as db:
        section_prices = [
            Theatre(section="A", prices=50.0),
            Theatre(section="B", prices=75.0),
            Theatre(section="C", prices=100.0)
        ]
        db.add_all(section_prices)
        db.commit()

    # Make a request to get all prices per theatre section
    response = client.get("/theatre/getallprices")

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response contains a list of dictionaries with "section" and "price"
    prices_resp = response.json()
    assert isinstance(prices_resp, list)
    assert len(prices_resp) == 6  

    # Assert each item in prices_resp has "section" and "price" keys
    expected_sections = {"A", "B", "C"}  # Assuming these are the sections we inserted
    for item in prices_resp:
        assert "section" in item
        assert "price" in item
        assert item["section"] in expected_sections

########################################################################################################

def test_create_section():
    # Define the payload for the new section
    new_section_data = {
        "section": "D",
        "seats": 150,
        "prices": 120.0
    }

    # Make a POST request to create a new section
    response = client.post("/theatre/createsection", json=new_section_data)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response contains the correct data
    section_resp = response.json()
    assert section_resp["section"] == new_section_data["section"]
    assert section_resp["seats"] == new_section_data["seats"]
    assert section_resp["prices"] == new_section_data["prices"]

    # Verify the section is in the database
    with TestingSessionLocal() as db:
        section_in_db = db.query(Theatre).filter(Theatre.section == new_section_data["section"]).first()
        assert section_in_db is not None
        assert section_in_db.section == new_section_data["section"]
        assert section_in_db.seats == new_section_data["seats"]
        assert section_in_db.prices == new_section_data["prices"]
