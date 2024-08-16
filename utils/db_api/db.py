import sqlite3
from aiogram.fsm.context import FSMContext

class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS USERS(
        full_name TEXT,
        telegram_id INTEGER unique );
              """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())


    def add_user(self, telegram_id:int, full_name:str):

        sql = """
        INSERT INTO Users(telegram_id, full_name) VALUES(?, ?);
        """
        self.execute(sql, parameters=(telegram_id, full_name), commit=True)


    def select_all_users(self):
        sql = """
        SELECT * FROM Users;
        """
        return self.execute(sql, fetchall=True)


    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE;"
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)


    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE;", commit=True)
    
    def all_users_id(self):
        return self.execute("SELECT telegram_id FROM Users;", fetchall=True)


class AnswersDatabase:
    def __init__(self, path_to_db="answers.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data  

    
    # Javoblarni olish uchun baza yaratyapmiz
    def create_table_user_answers(self):
        sql = """
        CREATE TABLE IF NOT EXISTS ANSWERS(
            full_name TEXT,
            telegram_id INTEGER unique,
            count INTEGER unique
        );
        """
        return self.execute(sql, commit=True)


        
    # add_user_answers bazaga foydalanuvchining javoblarni qo'shadi
    def add_user_answers(self, telegram_id:int, full_name:str, count:int):
        sql = """
        INSERT INTO ANSWERS(telegram_id, full_name, count) VALUES(?, ?, ?);
        """
        self.execute(sql, parameters=(telegram_id, full_name, count), commit=True)


    # count_users bazadan foydanalunuvchilarni sanash
    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM ANSWERS;", fetchone=True)
