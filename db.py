import sqlite3

def init_db():
    conn = sqlite3.connect("demo.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            city TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_data(name: str, age: int, city: str):
    conn = sqlite3.connect("demo.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO people (name, age, city) VALUES (?, ?, ?)",
        (name, age, city)
    )
    conn.commit()
    conn.close()

def run_query(sql_query: str):
    conn = sqlite3.connect("demo.db")
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
    except Exception as e:
        results = [f"Erro ao executar SQL: {e}"]
    conn.close()
    return results