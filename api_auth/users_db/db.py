from peewee import *
import platform
import json

class UsersDB():
    def __init__(self, db_path):
        self.db_path=db_path
        self.db = SqliteDatabase(self.db_path)
		
		
		#описание модели бд
        class Users(Model):
            class Meta:
                database=self.db
                table_name='Users'

            id = AutoField(primary_key=True)
            username=TextField()
            email=TextField()
            hashed_password=TextField()
        
        self.Users=Users()
        self.db.connect()
        self.db.create_tables([Users],)
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
        new_user=self.Users.create(username=username, email=email, hashed_password=hashed_password)
	
	#запрос на получение записи по username
    def get_user_by_username(self, username):
        query=self.Users.get_or_none(username=username)
        user=[query.id, query.username, query.email, query.hashed_password]
        return query


	#проверка что email не зарегистрирован
    def check_email(self, email):
        return self.Users.get_or_none(email=email)




