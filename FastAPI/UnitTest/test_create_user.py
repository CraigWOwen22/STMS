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