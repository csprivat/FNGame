
import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'port': int(os.getenv("DB_PORT", 3306)),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME"),
}

def insert_manual_entry():
    print("🔧 Inserção manual de pergunta no banco de dados")

    title = input("Título da publicação: ").strip()
    url = input("URL da publicação: ").strip()
    date_str = input("Data da publicação (DD/MM/AAAA): ").strip()

    try:
        created_at = datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("⚠️ Data inválida, usando data/hora atual.")
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    question_text = f"Publicação: \"{title}\". Ela é confiável?"
    option_1 = "Sim"
    option_2 = "Não"
    correct_answer = "Não"
    category = "Fake News"
    theme_id = 1  # Atualize se necessário

    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    insert_query = (
        "INSERT INTO questions "
        "(question_text, option_1, option_2, correct_answer, category, source, created_at, theme_id) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    )

    cursor.execute(insert_query, (
        question_text,
        option_1,
        option_2,
        correct_answer,
        category,
        url,
        created_at,
        theme_id
    ))

    connection.commit()
    cursor.close()
    connection.close()

    print("✅ Pergunta salva com sucesso!")

if __name__ == "__main__":
    insert_manual_entry()
