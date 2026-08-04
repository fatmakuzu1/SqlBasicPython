import sqlite3
import os

def create_database():
    if os.path.exists("students.db"):
        os.remove("students.db")

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    return conn,cursor

def create_tables(cursor):

    cursor.execute('''
        CREATE TABLE Students (
        id INTEGER PRIMARY KEY,
        name VARCHAR NOT NULL,
        age INTEGER,
        email VARCHAR UNIQUE NOT NULL,
        city VARCHAR
        )
    ''')
    cursor.execute('''
            CREATE TABLE Courses (
            id INTEGER PRIMARY KEY,
            course_name VARCHAR NOT NULL,
            instructor INTEGER
            
            )
        ''')
def main():
    conn,cursor = create_database()
    try:
        create_tables(cursor)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()

if __name__ =="__main__":
    main()