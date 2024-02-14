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



@auth_router.post('/register')
async def create_user(user: models.UserCreate):
    check_user=users.check_email(user.email)
    if check_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    salt=get_random_strings()
    hashed_password=hash_password(user.password, salt)
    users.add_user(user.username, user.email, hashed_password=f'{salt}.{hashed_password}')
    print('user created')


@auth_router.post('/login')
def login(data=Body()):
    login=data['login']
    user=users.get_user_by_username(login)

def check_email():
    pass
    
def check_token():
    pass

# случайные символы - соль
def get_random_strings(length=12):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))

def hash_password(password: str, salt: str = None):
    if salt is None:
        salt=get_random_strings()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()
    
#user=db.get_user_by_username('test_user_1')
#print(user.email)

#if __name__ == '__main__':
#    uvicorn.run(app='auth:auth_router')