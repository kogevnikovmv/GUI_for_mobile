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

        class Token(Model):
            class Meta:
                database=self.db
                table_name='Tokens'
            user=ForeignKeyField(Users, backref='token')
            token=TextField()
            #uid=UIDField()
            #date=DateField()

        self.db.connect()
        self.Users=Users()
        self.Token=Token()
        self.db.create_tables([Users, Token],)
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


	# ********Функции для проверки работы бд************

	#получение всех записей в бд
    def get_all_rows(self):
        cursor=self.db.cursor()
        cursor.execute('SELECT * FROM Users')
        result=cursor.fetchall()
        print(result)

	#получить названия всех таблиц бд
    def get_tables_names(self):
        list_names=self.db.get_tables()
        for name in list_names:
            print('table: ', name)
	
	#получить имена столбцов
    def get_fields(self):
        print(self.Users._meta.fields)

    def add_test_user(self):
        new_user = self.Users.create(username='test_user_1', email='test@test.ru', hashed_password='no_password')
        print('player add')


	# ************Функции для работы***********
    
    def add_user(self, username, email, hashed_password):
        user=self.Users.create(username=username, email=email, hashed_password=hashed_password)
        return user

    def create_token(self, user, token):
        self.Token.create(user=user, token=token)

	#запрос на получение записи по username
    def get_user_by_username(self, username):
        user=self.Users.get_or_none(username=username)
        #user=[user.id, user.username, user.email, user.hashed_password]
        return user


	#проверка что email не зарегистрирован
    def check_email(self, email):
        return self.Users.get_or_none(email=email)




