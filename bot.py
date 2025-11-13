import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from db import init_db, add_data, run_query

def ollama_generate(prompt: str, model: str = "llama3.1:8b") -> str:
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode("utf-8"),
        capture_output=True
    )
    return result.stdout.decode("utf-8").strip()

def text2sql(question: str):
    prompt = f"""
    Você é um gerador de SQL para SQLite.
    Regras:
    - Responda SOMENTE com a query SQL válida.
    - NÃO adicione ```sql ou qualquer markdown.
    - NÃO explique, apenas forneça a query.
    - Use apenas a tabela 'animais' com as colunas:
      id, nome, especie, idade, peso, habitat.

    Pergunta: {question}
    """
    sql_query = ollama_generate(prompt)
    print(f"[SQL Gerado] {sql_query}")
    resultados = run_query(sql_query)
    return sql_query, resultados

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! Sou um bot do zoológico que transforma texto em SQL.\n"
        "Envie uma pergunta, por exemplo:\n\n"
        "→ Quais animais vivem na Savana?\n"
        "→ Mostre o nome e o peso dos pinguins."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    await update.message.reply_text("Gerando SQL...")

    sql_query, resultados = text2sql(question)

    resposta = f"SQL gerado:\n{sql_query}\n\nResultado:\n{resultados}"
    await update.message.reply_text(resposta)

if __name__ == "__main__":
    import os

    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or "8319592448:AAGn1GKXBxilj2zKYe0DNtDb1zd_g9bDurg"

    init_db()
    add_data("Leão", "Panthera leo", 8, 190.5, "Savana")
    add_data("Girafa", "Giraffa camelopardalis", 12, 800.0, "Savana")
    add_data("Pinguim", "Aptenodytes forsteri", 5, 30.2, "Antártica")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot em execução")
    app.run_polling()