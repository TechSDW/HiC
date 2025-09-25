import sqlite3

def read():
    conn = sqlite3.connect("demo.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM people")
    results = cursor.fetchall()
    conn.close()
    return results