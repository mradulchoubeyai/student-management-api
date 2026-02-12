import sqlite3

DB_NAME = "students.db" #Creates a database file named students.db

def get_connection():    #Every time we call get_connection(), we get a fresh connection
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  #row_factory allows us to access rows like dictionaries
    return conn

def create_table(): #creates students table 
    conn = get_connection()
    cursor = conn.cursor()  #PRIMARY KEY enforces unique ID automatically & NOT NULL prevents empty values
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            marks TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()