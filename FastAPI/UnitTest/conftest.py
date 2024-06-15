# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from Main.database import Base, get_db
from Main.main import app
from sqlalchemy import create_engine


# Fixture to provide a test client for FastAPI app
@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

# Fixture to provide a test database session
@pytest.fixture(scope="function")
def test_db():
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(TESTING_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
