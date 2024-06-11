import sqlite3

class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        # Ma'lumotlar bazasiga ulanish
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        # SQL so'rovini bajarish uchun umumiy metod
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)  # So'rovni izohlash uchun logger funksiyasini qo'shamiz
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()  # O'zgarishlarni saqlash
        if fetchall:
            data = cursor.fetchall()  # Barcha natijalarni olish
        if fetchone:
            data = cursor.fetchone()  # Bir dona natijani olish
        connection.close()
        return data

    def create_table_users(self):
        # Foydalanuvchilar jadvalini yaratish
        sql = """
        CREATE TABLE IF NOT EXISTS Users(
        full_name TEXT,
        telegram_id NUMBER unique );
              """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        # SQL so'roviga parametrlarni qo'shish
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, telegram_id:int, full_name:str):
        # Yangi foydalanuvchi qo'shish
        sql = """
        INSERT INTO Users(telegram_id, full_name) VALUES(?, ?)
        """
        self.execute(sql, parameters=(telegram_id, full_name), commit=True)

    def select_all_users(self):
        # Barcha foydalanuvchilarni tanlash
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # Foydalanuvchini izlash
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        # Foydalanuvchilar sonini hisoblash
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def delete_users(self):
        # Barcha foydalanuvchilarni o'chirish
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)
    
    def all_users_id(self):
        # Barcha foydalanuvchilar ID larini tanlash
        return self.execute("SELECT telegram_id FROM Users;", fetchall=True)

    # Audio ma'lumotlari uchun metodlar

    def create_table_audios(self):
        # Audio jadvalini yaratish
        sql = """
        CREATE TABLE IF NOT EXISTS Audio(
        id INTEGER PRIMARY KEY,
        voice_file_id VARCHAR(50),
        title VARCHAR(20) 
           );
              """
        self.execute(sql, commit=True)

    def add_audio(self, voice_file_id:str, title:str):
        # Yangi audio qo'shish
        sql = """
        INSERT INTO Audio(voice_file_id, title) VALUES(?, ?)
        """
        self.execute(sql, parameters=(voice_file_id, title), commit=True)

    async def select_all_audios(self):
        # Barcha audio ma'lumotlarini tanlash
        sql = """
        SELECT * FROM Audio
        """
        return self.execute(sql, fetchall=True)

    async def search_audios_title(self, title):
        # Audio nomi bo'yicha qidirish
        sql = f"""
        SELECT * FROM Audio WHERE title LIKE "%{title}%"
        """
        return self.execute(sql, fetchall=True)

# SQL so'rovlarini konsolga chiqarish uchun logger
def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
