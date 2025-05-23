# -*- coding: utf-8 -*-
"""
Projeto: FNGame - Bot Educacional Anti Fake News
Autor: Cristian Privat
Apoio: Ricardo Andrade

Descrição:
Este módulo cuida da inserção de perguntas no banco de dados MariaDB.
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()

DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'port': int(os.getenv("DB_PORT", 3306)),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME"),
}

def insert_question(data_tuple, theme_id):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        query = (
            "INSERT INTO questions "
            "(question_text, option_1, option_2, correct_answer, category, source, theme_id) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )
        question_text, option_1, option_2, correct_answer, category, source = data_tuple
        cursor.execute(query, (question_text, option_1, option_2, correct_answer, category, source, theme_id))
        connection.commit()

    except mysql.connector.IntegrityError as e:
        print(f"❌ Erro ao inserir pergunta: {e}")
        if "a foreign key constraint fails" in str(e):
            print(f"💡 Dica: O valor de 'theme_id={theme_id}' não existe na tabela 'themes'.")

    except Error as e:
        print("❌ Erro no banco de dados:", e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()


def get_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print("❌ Erro ao conectar no banco de dados:", e)
        return None


def fetch_questions(theme_id):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT question_text, option_1, option_2, correct_answer
            FROM questions
            WHERE theme_id = %s
            ORDER BY RAND()
            LIMIT 20
        """, (theme_id,))
        results = cursor.fetchall()
        questions = [
            {
                "question": row["question_text"],
                "options": [row["option_1"], row["option_2"]],
                "answer": row["correct_answer"]
            }
            for row in results
        ]
        return questions
    except Error as e:
        print("Erro ao buscar perguntas:", e)
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
