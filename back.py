from tkinter.font import nametofont

from fastapi import FastAPI
from script import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
app = FastAPI()

oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="Login")
password_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")

class check_room(BaseModel):
    current_room : int
    destination_room : int
    id : int

class users(BaseModel):
    username : str
    regno : str
@app.get("/path")
def get_path():
    return {"Path": "Here's the path to the your destination room"}
@app.post("/post")
def enter_post(room):

    return {"Message ": f"received your destination room. You will be shown the path in a few seconds"}

users={"name": "Moksh","Registration Number": "25BDS0129"}
@app.post("/login"):
def login():

    return {"Message": "Login successful"}
@app.post("/signup")


