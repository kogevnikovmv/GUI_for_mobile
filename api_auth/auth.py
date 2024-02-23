from fastapi import APIRouter, Body, HTTPException
from api_auth.users_db import db
from api_auth import models
from api_auth.config import DbPath

import hashlib
import random
import string

#import uvicorn

users=db.UsersDB(DbPath.WIN_PATH)

auth_router=APIRouter()

@auth_router.on_event('startup')
def db_connect():
    users.connect()
    print('db connected')
    
@auth_router.on_event('shutdown')
def db_close():
    users.close()
    print('db closed')



@auth_router.post('/register', response_model=models.UserToken)
async def create_user(user: models.UserCreate):
    check_email=users.get_user_by_email(user.email)
    if check_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    check_username=users.get_user_by_username(user.username)
    if check_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    salt=get_random_strings()
    hashed_password=hash_password(user.password, salt)
    user=users.add_user(user.username, user.email, hashed_password=f'{salt}.{hashed_password}')
    token=create_user_token(user)

    return {'sub': user.id, 'token': token}



@auth_router.post('/login', response_model=models.UserToken)
async def login(credentials: models.UserLogin):
    user=users.get_user_by_username(credentials.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username/password")
    if not check_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username/password")
    token = create_user_token(user)

    return {'sub': user.id, 'token': token}

def check_password(user_password, hashed):
    salt, hashed_password=hashed.split('.')
    return hash_password(user_password, salt)==hashed_password


def check_token():
    pass

def create_user_token(user):
    token=users.create_token(user)
    return {'token_type': 'bearer', 'token': token}


# случайные символы - соль
def get_random_strings(length=12):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))

def hash_password(password: str, salt: str = None):
    if salt is None:
        salt=get_random_strings()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()
