import sqlite3

# Database (Ma'lumotlar bazasi) sinfini yaratamiz
# class Database:
#     def __init__(self, path_to_db="main.db"):
#         self.path_to_db = path_to_db

#     # Ma'lumotlar bazasiga ulanish xususiyati
#     @property
#     def connection(self):
#         return sqlite3.connect(self.path_to_db)

#     # SQL buyruqlarini bajarish metodi
#     def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
#         if not parameters:
#             parameters = ()
        
#         connection = self.connection
#         cursor = connection.cursor()

#         try:
#             cursor.execute(sql, parameters)

#             if commit:
#                 connection.commit()
#             if fetchall:
#                 data = cursor.fetchall()
#             elif fetchone:
#                 data = cursor.fetchone()
#             else:
#                 data = None

#             return data
        
#         except Exception as e:
#             print(f"Error executing SQL query: {e}")
        
#         finally:
#             connection.close()

#     # Foydalanuvchilar jadvalini yaratish
#     def create_table_users(self):
#         sql = """
#         CREATE TABLE IF NOT EXISTS Users(
#             telegram_id INTEGER PRIMARY KEY,
#             full_name TEXT UNIQUE
#         )
#         """
#         self.execute(sql, commit=True)

#     # Yangi foydalanuvchini qo'shish
#     def add_user(self, telegram_id: int, full_name: str):
#         sql = """
#         INSERT INTO Users(telegram_id, full_name) VALUES(?, ?)
#         """
#         self.execute(sql, parameters=(telegram_id, full_name), commit=True)

#     # Barcha foydalanuvchilarni tanlash
#     def select_all_users(self):
#         sql = """
#         SELECT * FROM Users
#         """
#         return self.execute(sql, fetchall=True)

#     # Muayyan foydalanuvchini tanlash
#     def select_user(self, **kwargs):
#         sql = "SELECT * FROM Users WHERE "
#         sql, parameters = self.format_args(sql, kwargs)
#         return self.execute(sql, parameters=parameters, fetchone=True)

#     # Foydalanuvchilar sonini sanash
#     def count_users(self):
#         return self.execute("SELECT COUNT(*) FROM Users", fetchone=True)

#     # Barcha foydalanuvchilarni o'chirish
#     def delete_users(self):
#         self.execute("DELETE FROM Users", commit=True)

#     # Barcha foydalanuvchilar IDlarini olish
#     def all_users_id(self):
#         return self.execute("SELECT telegram_id FROM Users", fetchall=True)

#     # Nomzodlar jadvalini yaratish
#     def create_table_candidates(self):
#         sql = """
#         CREATE TABLE IF NOT EXISTS Candidates(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             telegram_id INTEGER,
#             full_name TEXT,
#             district TEXT,
#             neighborhood TEXT,
#             vote_place TEXT,
#             rating INTEGER DEFAULT 0,  -- Reyting ustunini 0 standart qiymat bilan ta'minlash
#             FOREIGN KEY(telegram_id) REFERENCES Users(telegram_id)
#         )
#         """
#         self.execute(sql, commit=True)

#     # Nomzodning reytingini oshirish
#     def increment_candidate_score(self, candidate_id):
#         sql = """
#         UPDATE Candidates
#         SET rating = COALESCE(rating, 0) + 1
#         WHERE id = ?
#         """
#         self.execute(sql, parameters=(candidate_id,), commit=True)

#     # Yangi nomzod qo'shish
#     def add_candidate(self, telegram_id: int, full_name: str, district: str, neighborhood: str, vote_place: str):
#         sql = """
#         INSERT INTO Candidates(telegram_id, full_name, district, neighborhood, vote_place) 
#         VALUES(?, ?, ?, ?, ?)
#         """
#         self.execute(sql, parameters=(telegram_id, full_name, district, neighborhood, vote_place), commit=True)

#     # Barcha nomzodlarni tanlash
#     def select_all_candidates(self):
#         sql = """
#         SELECT * FROM Candidates
#         """
#         return self.execute(sql, fetchall=True)

#     # Muayyan nomzodni tanlash
#     def select_candidate(self, **kwargs):
#         sql = "SELECT * FROM Candidates WHERE "
#         sql, parameters = self.format_args(sql, kwargs)
#         return self.execute(sql, parameters=parameters, fetchone=True)

#     # Barcha nomzodlarni o'chirish
#     def delete_candidates(self):
#         self.execute("DELETE FROM Candidates", commit=True)

#     # Nomzodlarni sahifalab olish
#     def get_candidates_paginated(self, limit: int, offset: int):
#         sql = """
#         SELECT * FROM Candidates LIMIT ? OFFSET ?
#         """
#         return self.execute(sql, parameters=(limit, offset), fetchall=True)
    
#     # Muayyan joylashuvdagi nomzodlarni tanlash
#     def get_candidates_by_location(self, district, neighborhood):
#         sql = """
#         SELECT * FROM Candidates WHERE district = ? AND neighborhood = ?
#         """
#         return self.execute(sql, parameters=(district, neighborhood), fetchall=True)

#     # Nomzodlar sonini sanash
#     def count_candidates(self):
#         return self.execute("SELECT COUNT(*) FROM Candidates", fetchone=True)
    
#     # Muayyan joylashuvdagi bolalar bog'chalari ro'yxatini olish
#     def get_kinder_schools_by_location(self, district, neighborhood):
#         query = """
#         SELECT DISTINCT vote_place 
#         FROM Candidates 
#         WHERE district = ? AND neighborhood = ?
#         """
#         return self.execute(query, (district, neighborhood), fetchall=True)

#     # Muayyan joylashuvdagi va bolalar bog'chasidagi nomzodlarni tanlash
#     def get_candidates_by_location(self, district, neighborhood, kindergarten_school):
#         query = """
#         SELECT * 
#         FROM Candidates 
#         WHERE district = ? AND neighborhood = ? AND vote_place = ?
#         """
#         return self.execute(query, (district, neighborhood, kindergarten_school), fetchall=True)
    
#     # Muayyan nomzodni tanlash
#     def select_candidate(self, **kwargs):
#         sql = "SELECT * FROM Candidates WHERE "
#         sql, parameters = self.format_args(sql, kwargs)
#         return self.execute(sql, parameters=parameters, fetchone=True)

#     # Telegram ID orqali nomzod ID sini olish
#     def get_candidate_id_by_telegram_id(self, telegram_id):
#         sql = """
#         SELECT id FROM Candidates WHERE telegram_id = ?
#         """
#         return self.execute(sql, parameters=(telegram_id,), fetchone=True)
    
#     # Barcha nomzodlarni reytinglari bilan birga olish
#     def get_all_candidates_with_ratings(self):
#         sql = """
#         SELECT Candidates.id, Candidates.full_name, Candidates.district, Candidates.neighborhood, Candidates.vote_place,
#                AVG(Ratings.rating) AS average_rating
#         FROM Candidates
#         LEFT JOIN Ratings ON Candidates.id = Ratings.candidate_id
#         GROUP BY Candidates.id
#         """
#         return self.execute(sql, fetchall=True)

#     # SQL buyruqlarni formatlash uchun yordamchi funksiya
#     @staticmethod
#     def format_args(sql, parameters: dict):
#         sql += " AND ".join([
#             f"{item} = ?" for item in parameters
#         ])
#         return sql, tuple(parameters.values())
    

# # SQL buyruqlarni chop etish uchun logger funksiyasi
# def logger(statement):
#     print(f"""
# _____________________________________________________        
# Executing: 
# {statement}
# _____________________________________________________
# """)

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

        try:
            cursor.execute(sql, parameters)

            if commit:
                connection.commit()
            if fetchall:
                data = cursor.fetchall()
            elif fetchone:
                data = cursor.fetchone()
            else:
                data = None

            return data
        
        except Exception as e:
            print(f"Error executing SQL query: {e}")
        
        finally:
            connection.close()

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users(
            telegram_id INTEGER PRIMARY KEY,
            full_name TEXT UNIQUE
        )
        """
        self.execute(sql, commit=True)

    def add_user(self, telegram_id: int, full_name: str):
        sql = """
        INSERT INTO Users(telegram_id, full_name) VALUES(?, ?)
        """
        self.execute(sql, parameters=(telegram_id, full_name), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users", fetchone=True)

    def delete_users(self):
        self.execute("DELETE FROM Users", commit=True)

    def all_users_id(self):
        return self.execute("SELECT telegram_id FROM Users", fetchall=True)

    def create_table_candidates(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Candidates(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            full_name TEXT,
            district TEXT,
            neighborhood TEXT,
            vote_place TEXT,
            rating INTEGER DEFAULT 0,
            FOREIGN KEY(telegram_id) REFERENCES Users(telegram_id)
        )
        """
        self.execute(sql, commit=True)

    def increment_candidate_score(self, candidate_id):
        sql = """
        UPDATE Candidates
        SET rating = COALESCE(rating, 0) + 1
        WHERE id = ?
        """
        self.execute(sql, parameters=(candidate_id,), commit=True)

    def add_candidate(self, telegram_id: int, full_name: str, district: str, neighborhood: str, vote_place: str):
        sql = """
        INSERT INTO Candidates(telegram_id, full_name, district, neighborhood, vote_place) 
        VALUES(?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(telegram_id, full_name, district, neighborhood, vote_place), commit=True)

    def select_all_candidates(self):
        sql = """
        SELECT * FROM Candidates
        """
        return self.execute(sql, fetchall=True)

    def select_candidate(self, **kwargs):
        sql = "SELECT * FROM Candidates WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def delete_candidates(self):
        self.execute("DELETE FROM Candidates", commit=True)

    def get_candidates_paginated(self, limit: int, offset: int):
        sql = """
        SELECT * FROM Candidates LIMIT ? OFFSET ?
        """
        return self.execute(sql, parameters=(limit, offset), fetchall=True)

    def get_candidates_by_location(self, district, neighborhood):
        sql = """
        SELECT * FROM Candidates WHERE district = ? AND neighborhood = ?
        """
        return self.execute(sql, parameters=(district, neighborhood), fetchall=True)

    def count_candidates(self):
        return self.execute("SELECT COUNT(*) FROM Candidates", fetchone=True)

    def get_kinder_schools_by_location(self, district, neighborhood):
        query = """
        SELECT DISTINCT vote_place 
        FROM Candidates 
        WHERE district = ? AND neighborhood = ?
        """
        return self.execute(query, (district, neighborhood), fetchall=True)

    def get_candidates_by_location(self, district, neighborhood, kindergarten_school):
        query = """
        SELECT * 
        FROM Candidates 
        WHERE district = ? AND neighborhood = ? AND vote_place = ?
        """
        return self.execute(query, (district, neighborhood, kindergarten_school), fetchall=True)

    def select_candidate(self, **kwargs):
        sql = "SELECT * FROM Candidates WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def get_candidate_id_by_telegram_id(self, telegram_id):
        sql = """
        SELECT id FROM Candidates WHERE telegram_id = ?
        """
        return self.execute(sql, parameters=(telegram_id,), fetchone=True)

    def get_all_candidates_with_ratings(self):
        sql = """
        SELECT Candidates.id, Candidates.full_name, Candidates.district, Candidates.neighborhood, Candidates.vote_place,
               AVG(Ratings.rating) AS average_rating
        FROM Candidates
        LEFT JOIN Ratings ON Candidates.id = Ratings.candidate_id
        GROUP BY Candidates.id
        """
        return self.execute(sql, fetchall=True)

    def create_table_ratings(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Ratings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            rating INTEGER,
            FOREIGN KEY(candidate_id) REFERENCES Candidates(id)
        )
        """
        self.execute(sql, commit=True)

    def add_rating(self, candidate_id: int, rating: int):
        sql = """
        INSERT INTO Ratings(candidate_id, rating) VALUES(?, ?)
        """
        self.execute(sql, parameters=(candidate_id, rating), commit=True)

    @property
    def top_rating(self):
        sql = """SELECT  * FROM Candidates ORDER BY RATING DESC"""
        return self.execute(sql, fetchall=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())
