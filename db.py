import sqlite3

def init_db():
    conn = sqlite3.connect("zoologico.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS animais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            especie TEXT NOT NULL,
            idade INTEGER,
            peso REAL,
            habitat TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_data(nome: str, especie: str, idade: int, peso: float, habitat: str):
    conn = sqlite3.connect("zoologico.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO animais (nome, especie, idade, peso, habitat) VALUES (?, ?, ?, ?, ?)",
        (nome, especie, idade, peso, habitat)
    )
    conn.commit()
    conn.close()

def delete_data(parametro: str):
    conn = sqlite3.connect("zoologico.db")
    cursor = conn.cursor()
    if parametro.isdigit():
        cursor.execute("DELETE FROM animais WHERE id = ?", (parametro,))
    else:
        cursor.execute("DELETE FROM animais WHERE nome LIKE ?", (f"%{parametro}%",))
    conn.commit()
    conn.close()

def update_data(id_animal: int, campo: str, novo_valor):
    conn = sqlite3.connect("zoologico.db")
    cursor = conn.cursor()
    query = f"UPDATE animais SET {campo} = ? WHERE id = ?"
    cursor.execute(query, (novo_valor, id_animal))
    conn.commit()
    conn.close()

def run_query(sql_query: str):
    conn = sqlite3.connect("zoologico.db")
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        resultados = cursor.fetchall()
    except Exception as e:
        resultados = [f"Erro ao executar SQL: {e}"]
    conn.close()
    return resultados