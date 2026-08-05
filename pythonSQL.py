# Temel SQL Komutları
# SELECT * FROM Students;
# SELECT id, name, age FROM Students;
# SELECT * FROM Students WHERE city = 'new york';
# INSERT INTO Students (id, name, age, email, city) VALUES (6, 'zeynep', 23, 'zeynep@gmail.com', 'istanbul');
# UPDATE Students SET city = 'ankara' WHERE id = 1;
# DELETE FROM Students WHERE id = 6;
# SELECT * FROM Courses;
# SELECT course_name, instructor FROM Courses WHERE credits > 2;
# ALTER TABLE Students ADD COLUMN phone VARCHAR;
# DROP TABLE Students;
# CREATE TABLE Students (id INTEGER PRIMARY KEY, name VARCHAR NOT NULL, age INTEGER, email VARCHAR UNIQUE NOT NULL, city VARCHAR);
# JOIN örneği: SELECT s.name, c.course_name FROM Students s JOIN Courses c ON s.id = c.id;

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
            instructor INTEGER,
            credits INTEGER
            
            )
        ''')

def insert_sample_data(cursor):
    students = [
        (1,'alice johnson',20,'alicej@gmail.com','new york'),
        (2,'bob türk',19,'bobtürk@gmail.com','chicago'),
        (3,'can white',21,'canw@gmail.com','boston'),
        (4,'david brown',20,'davidb@gmail.com','new york'),
        (5,'erling haaland',22,'erling@gmail.com','seattle')
    ]
    cursor.executemany("INSERT INTO Students VALUES (?,?,?,?,?)",students) # soru işareti sql syntaxında olan bir şey

    coursers = [
        (1,'python programming','dr. anderson',3),
        (2,'java programming','dr. white',4),
        (3,'c++ programming','dr. brown',3),
        (4,'c# programming','dr. black',2)
    ]
    cursor.executemany("INSERT INTO Courses VALUES (?,?,?,?)",coursers)
    print("studnts inserted successfully")

def basic_sql_operations(cursor):
    #SELECET ALL
    print("----------select all-------")
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()
    for row in records:
        print(row)

    # SELECT Columns
    print("----------select columns-------")
    cursor.execute("SELECT name,age FROM students")
    records = cursor.fetchall()
    print(records)

    # WHERE Clause
    print("----------where clause-------")
    cursor.execute("SELECT * FROM students WHERE age>=20")
    records = cursor.fetchall()
    print(records)

    # ORDER BY
    print("----------ORDER BY-------")
    cursor.execute("SELECT * FROM students ORDER BY age")
    records = cursor.fetchall()
    print(records)

    # LIMIT
    print("----------LİMİT BY 3-------")
    cursor.execute("SELECT * FROM students LIMIT 3")
    records = cursor.fetchall()
    print(records)


def sql_update_delete_insert_operations(conn,cursor):
    #INSERT
    cursor.execute("INSERT INTO students (id,name,age,email,city) VALUES (6,'frank miller',23,'frank@gmail.com','miami')")
    conn.commit()

    #update
    cursor.execute("UPDATE students SET age = 27 WHERE id= 6")
    conn.commit()

    #delete
    cursor.execute("DELETE FROM students WHERE id =3")

def aggregate_func(cursor):

    #count
    cursor.execute("SELECT COUNT(*) FROM students")
    result = cursor.fetchone()#tek sonuç verir fetchall lise içinde tuple verir
    print(result[0])

    #average
    cursor.execute("SELECT AVG(age) FROM students")
    result = cursor.fetchone()
    print(result[0])

    #max-min
    cursor.execute("SELECT MAX(age) FROM students")
    result = cursor.fetchone()
    print(result[0])

    cursor.execute("SELECT MIN(age) FROM students")
    result = cursor.fetchone()
    print(result[0])

    #group by
    cursor.execute("SELECT city , COUNT(*) FROM students GROUP BY city")
    result = cursor.fetchall()
    print(result)

def answers(cursor):
    cursor.execute("SELECT * FROM students")
    cursor.fetchall()
    cursor.execute("SELECT course_name, instructor FROM Courses")
    cursor.fetchall()
    cursor.execute("SELECT * FROM students WHERE age>21")
    cursor.fetchall()
    cursor.execute("SELECT * FROM students WHERE city = 'chicago'")
    cursor.fetchall()
    cursor.execute("SELECT * FROM Courses WHERE instructor='dr.anderson'")
    cursor.fetchall()
    cursor.execute("SELECT * FROM students WHERE name LIKE 'a%'")
    cursor.fetchall()
    cursor.execute("SELECT * FROM Courses WHERE credits >=3")
    cursor.fetchall()
    cursor.execute("SELECT * FROM students ORDER BY name")
    cursor.fetchall()
    cursor.execute("SELECT name,age FROM students WHERE age >20 ORDER BY name")
    cursor.fetchall()
    cursor.execute("SELECT name ,city FROM students  WHERE city IN ('new york,chicago')")
    cursor.fetchall()
    cursor.execute("SELECT name,city FROM students WHERE city != 'new york'")
    cursor.fetchall()
    

    

def main():
    conn,cursor = create_database()
    try:
        create_tables(cursor)
        insert_sample_data(cursor)
        basic_sql_operations(cursor)
        sql_update_delete_insert_operations(conn,cursor)
        aggregate_func(cursor)
        answers(cursor)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()

if __name__ =="__main__":
    main()