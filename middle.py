from time import time
from typing import Annotated
from fastapi import FastAPI, HTTPException, Body, status, Request
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, EmailStr

app = FastAPI()


"""
1. firstname
2. lastname
3. age
4. email
5. height
"""
user_db = { "Muli": {"firstname": "Mulikat", "lastname": "Giwa", "age": 35, "email": "muli@yahoomail.com", "height": "5.6ft"}}

class User(BaseModel):
    firstname:str
    lastname:str
    age:int
    email:EmailStr
    height:str
    

@app.middleware("http")
async def log_request(request:Request, call_next):
    start_time = time()
    response = await call_next(request)

    duration = time() - start_time
    log_info = {"duration":duration, "Request":request.method, "Status":response.status_code}
    print(log_info)

    return response

origins = [
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/signup",status_code=status.HTTP_201_CREATED)
async def sign_up(user:Annotated[User, Body()]):
    for Id, user_profile in user_db.items():
        if user_profile["email"] == user.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exist")
        
    user_db[user.email] = user.model_dump()

    return "Signup Successful"