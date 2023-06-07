import sqlite3 as sq
conn =sq.connect('Database/Reports.db')
c= conn.cursor()
c.execute("DROP TABLE students")
c.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    gender TEXT,
                    mobile TEXT,
                    website TEXT,
                    dob TEXT,
                    address TEXT,
                    email TEXT,
                    remarks TEXT,
                    photo BLOB)''')
conn.commit()
conn.close()