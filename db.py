import sqlite3

# 🔹 Inicializa o banco de dados e cria a tabela de animais
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


# 🔹 Adiciona um novo animal
def add_data(nome: str, especie: str, idade: int, peso: float, habitat: str):
    conn = sqlite3.connect("zoologico.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO animais (nome, especie, idade, peso, habitat) VALUES (?, ?, ?, ?, ?)",
        (nome, especie, idade, peso, habitat)
    )
    conn.commit()
    conn.close()


# 🔹 Executa uma query SQL (SELECT, UPDATE, DELETE etc)
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

if __name__ == "__main__":
    init_db()

    add_data("Leão", "Panthera leo", 8, 190.5, "Savana")
    add_data("Girafa", "Giraffa camelopardalis", 12, 800.0, "Savana")
    add_data("Pinguim", "Aptenodytes forsteri", 5, 30.2, "Antártica")

    animais = run_query("SELECT * FROM animais")
    for a in animais:
        print(a)