# tests/test_login.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from Main.models import User
from Main.services import createUser, decryptAccessToken
from Main.schemas import UserCreate

SECRET_KEY = "Thomas"

def test_login(test_client: TestClient, test_db: Session):
    user_create_data = {
        "username": "IZAN2",
        "password": "IZAN2"
    }


    # Create the user in the test database
    createUser(db=test_db, userData=user_create_data)

    # Make the login request
    response = test_client.post("/authentication/login", json=user_create_data)
    print("HERE", response.json())

    # Assert the status code is 200 (OK)
    assert response.status_code == 200


    access_token = response.json().get("access_token")
    

   
    assert access_token is not None, "Access token not found in response"

   


    print("access_token", access_token)
    decoded_token = decryptAccessToken(access_token)

    assert "userID" in decoded_token, "User ID not found in decoded token"

    print("DECODED", decoded_token)
    assert decoded_token["userID"] == 1, "Expected user ID does not match"






