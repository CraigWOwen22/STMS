from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from Main.database import Base, get_db
from Main.main import app
from Main.schemas import UserCreate
from Main.services import createUser, hashing  # Assuming createUser function and hashing is imported from services module
from Main.models import User  # Assuming User model is imported from models module

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
