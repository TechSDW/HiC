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
    - Use apenas a tabela 'people' com as colunas: id, name, age, city.
    
    Pergunta: {question}
    """
    sql_query = ollama_generate(prompt)
    print(f"[SQL Gerado] {sql_query}")
    results = run_query(sql_query)
    return sql_query, results

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! Sou um bot que transforma texto em SQL.\n"
        "Envie uma pergunta, por exemplo:\n\n"
        "→ Quem mora em São Paulo?"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    await update.message.reply_text("Gerando SQL... (pode demorar um pouco)")

    sql_query, results = text2sql(question)
    response = f"SQL gerado:\n{sql_query}\n\nResultado:\n{results}"
    await update.message.reply_text(response)

if __name__ == "__main__":
    import os

    # seu token do BotFather aqui
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or "token"

    init_db()
    add_data("Alice", 25, "São Paulo")
    add_data("Bruno", 30, "Rio de Janeiro")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot em execução")
    app.run_polling()