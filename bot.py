import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from db import init_db, add_data, delete_data, update_data, run_query

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
    print(f"Resposta do SQL: {resultados}")
    return sql_query, resultados

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bem-vindo ao Bot do Zoológico!\n\n"
        "Comandos disponíveis:\n"
        "/add <nome> <espécie> <idade> <peso> <habitat>\n"
        "/delete <id_ou_nome>\n"
        "/update <id> <campo> <novo_valor>\n"
        "/listar\n\n"
        "Ou envie uma pergunta, por exemplo:\n"
        "→ Quais animais vivem na Savana?"
    )

async def add_animal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        nome, especie, idade, peso, habitat = context.args
        idade = int(idade)
        peso = float(peso)
        add_data(nome, especie, idade, peso, habitat)
        await update.message.reply_text(f"Animal '{nome}' adicionado com sucesso!")
    except ValueError:
        await update.message.reply_text("Uso incorreto. Exemplo:\n/add Leão Panthera_leo 8 190.5 Savana")
    except Exception as e:
        await update.message.reply_text(f"Erro ao adicionar: {e}")

async def delete_animal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /delete <id_ou_nome>")
        return
    parametro = " ".join(context.args)
    delete_data(parametro)
    await update.message.reply_text(f"Animal '{parametro}' removido (se existia).")

async def update_animal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text("Uso: /update <id> <campo> <novo_valor>")
        return

    id_animal, campo, novo_valor = context.args[0], context.args[1], " ".join(context.args[2:])
    campos_validos = ["nome", "especie", "idade", "peso", "habitat"]

    if campo not in campos_validos:
        await update.message.reply_text(f"Campo inválido! Use: {', '.join(campos_validos)}")
        return

    if campo == "idade":
        novo_valor = int(novo_valor)
    elif campo == "peso":
        novo_valor = float(novo_valor)

    update_data(id_animal, campo, novo_valor)
    await update.message.reply_text(f"Animal {id_animal} atualizado: {campo} = {novo_valor}")

async def listar_animais(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resultados = run_query("SELECT * FROM animais")
    if not resultados:
        await update.message.reply_text("Nenhum animal encontrado.")
    else:
        resposta = "Lista de Animais:\n\n"
        for r in resultados:
            resposta += f"ID: {r[0]} | Nome: {r[1]} | Espécie: {r[2]} | Idade: {r[3]} | Peso: {r[4]} | Habitat: {r[5]}\n"
        await update.message.reply_text(resposta)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    await update.message.reply_text("Processando sua pergunta...")
    sql_query, resultados = text2sql(question)
    resposta = f"SQL gerado:\n{sql_query}\n\nResultado:\n{resultados}"
    await update.message.reply_text(resposta)

if __name__ == "__main__":
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or "8319592448:AAGn1GKXBxilj2zKYe0DNtDb1zd_g9bDurg"

    init_db()

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_animal))
    app.add_handler(CommandHandler("delete", delete_animal))
    app.add_handler(CommandHandler("update", update_animal))
    app.add_handler(CommandHandler("listar", listar_animais))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot do Zoológico em execução... Pressione Ctrl+C para parar.")
    app.run_polling()