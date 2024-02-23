from peewee import *
import uuid
from datetime import datetime

class UIDField(Field):
    db_field='uid'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default=uuid.uuid4

    def db_value(self, value):
        return str(value)
    def python_value(self, value):
        return uuid.UUID(value)

class UsersDB():
    def __init__(self, db_path):
        self.db_path=db_path
        self.db = SqliteDatabase(self.db_path)
		
		
		#описание модели бд
        class Users(Model):
            class Meta:
                database=self.db
                table_name='Users'

            username=TextField()
            email=TextField()
            hashed_password=TextField()

        class Tokens(Model):
            class Meta:
                database=self.db
                table_name='Tokens'
            user_id=ForeignKeyField(Users, backref='tokens')
            token=UIDField()
            #date=DateField()

        self.db.connect()
        self.Users=Users()
        self.Tokens=Tokens()
        self.db.create_tables([Users, Tokens],)
        self.db.close()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
        print('db closed')
	
    def close(self):
        self.db.close()
		
    def connect(self):
        self.db.connect()

    
    def add_user(self, username, email, hashed_password):
        user=self.Users.create(username=username, email=email, hashed_password=hashed_password)
        return user

    def create_token(self, user):
        token=self.Tokens.get_or_none(user_id=user.id)
        if token:
            token.token=uuid.uuid4()
        else:
            token=self.Tokens.create(user_id=user.id)
        return token.token

	#запрос на получение записи по username
    def get_user_by_username(self, username):
        user=self.Users.get_or_none(username=username)
        return user

    def get_user_by_email(self, email):
        user = self.Users.get_or_none(email=email)
        return user



