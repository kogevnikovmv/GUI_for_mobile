from fastapi import APIRouter, Body, HTTPException
from database.database import UsersDB
import models

import hashlib
import random
import string

db=UsersDB()

auth_router=APIRouter()

@auth_router.on_event('startup')
async def db_connect():
    await db.connect()
    print('db connected')
    
@auth_router.on_event('shutdown')
async def db_close():
    await db.close()
    print('db closed')



@auth_router.post('/register')
async def create_user(user: models.UserCreate):
    check_user=db.check_email(user.email)
    if check_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    salt=get_random_strings()
    hashed_password=hash_password(user.password, salt)
    db.add_user(user.username, user.email, hashed_password=f'{salt}.{hashed_password}')
    print('user created')


@auth_router.post('/login')
def login(data=Body()):
    login=data['login']
    user=db.get_user_by_username(login)

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