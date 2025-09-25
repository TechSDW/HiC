import sqlite3
import subprocess

import mainApp

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

def ollama_generate(prompt: str, model: str = "qwen2.5-coder:3b") -> str:
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode("utf-8"),
        capture_output=True
    )

    return result.stdout.decode("utf-8").strip()

def text2sql(question: str) -> list:
    prompt = f"""
        Você é um gerador de SQL para SQLite.
        Regras IMPORTANTES:
        - Responda SOMENTE com a query SQL válida.
        - NÃO adicione ```sql ou qualquer markdown.
        - NÃO explique, apenas forneça a query.
        - Use apenas a tabela 'people' com as colunas: id, name, age, city.

        Pergunta: {question}
        """
    
    sql_query = ollama_generate(prompt)
    print("SQL gerado:", sql_query)

    conn = sqlite3.connect("demo.db")
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
    except Exception as e:
        results = [f"Erro ao executar SQL: {e}"]
    conn.close()

    return results

def add_data(name: str, age: int, city: str) -> bool:
    conn = sqlite3.connect("demo.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO people (name, age, city) VALUES (?, ?, ?)",
        (name, age, city)
    )
    conn.commit()
    conn.close()
    return True

if __name__ == "__main__":
    print("1 - Visualizar banco de dados;\n" +
          "2 - Adicionar animal;\n" +
          "3 - Atualizar animal;\n" +
          "4 - Remover animal;\n" +
          "5 - Sair")

    while True:
        options = input("O que deseja fazer?: ")

        match options:
            case "1":
                mainApp.read()
                break
            case "2":
                print("Caso 2 ahahahhaa")
                break
            case "3":
                print("Caso 3 ahahahhaa")
                break
            case "4":
                print("Caso 4 ahahahhaa")
                break
            case "5":
                print("Caso 5 ahahahhaa")
                break
            case _:
                print("Número inválido, digite outro número")
    init_db()

    add_data("Alice", 25, "São Paulo")
    add_data("Bruno", 30, "Rio de Janeiro")

    pergunta = "Quais pessoas moram em São Paulo?"
    print("Resposta para:", pergunta)
    print(text2sql(pergunta))