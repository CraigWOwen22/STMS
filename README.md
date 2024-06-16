# FastAPI Project

Welcome to the my first FastAPI/React project repository! This project demonstrates a basic simple ticket management system.

## Getting Started 

To get a local copy of this project up and running, follow these simple steps.

Run the following git command:
git clone https://github.com/CraigWOwen22/STMS.git

Navigate to STMS/FastAPI directory:
cd STMS/FastAPI

Activate the environment:
"source env/bin/activate"

Run the following command to install dependancies:
"pip install -r requirements.txt"

Run the command to start server:
uvicorn Main.main:app --reload

Open a browser and navigate to this address:
"http://localhost:8000/docs" ( or any equivalent e.g. postman )

Create a user with the users/create API and send the following payload:
{
  "username": "rootuser",
  "password": "Password"
}

Populate the Theatre table with the theatre/createsection API endpoint and using these 3 payloads:
{
  "section": "A",
  "seats": 20,
  "prices": 50
}
{
  "section": "B",
  "seats": 30,
  "prices": 30
}
{
  "section": "C",
  "seats": 50,
  "prices": 20
}

In a new terminal, navigate to stms-app:
cd STMS/React/stms-app

Start react with the command:
npm start

In a browser, navigate to the following address:
http://localhost:3000

At this address should be the User interface to the app

Use the credentials for username and password, "rootuser" and "Password" respectively.
Once logged into the system you can view any current bookings, create new bookings,
and remove any bookings.

### Prerequisites

Make sure you have Python and pip installed on your machine. 

```bash
python --version  # Python 3.7+
pip --version     # pip 21.0+


Testing the APIS

Run the following command in the FastAPI dir
"PYTHONPATH=$(pwd) pytest UnitTest/test_api.py"








pip install fastapi pytest httpx pytest-asyncio


pytest -v test_api.py

uvicorn Main.main:app --reload





