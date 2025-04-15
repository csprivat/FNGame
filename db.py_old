# -*- coding: utf-8 -*-
"""
Projeto: FNGame - Bot Educacional Anti Fake News
Autor: Cristian Privat
Apoio: Ricardo Andrade

Descrição:
Este script faz parte do projeto FNGame, uma iniciativa educacional
para combater a desinformação através de um quiz interativo.
Os dados utilizados são obtidos de fontes públicas com fins didáticos.

Licença:
Este projeto é licenciado sob a Licença Pública Geral Affero GNU v3 (AGPLv3).
Qualquer redistribuição deve manter o código-fonte aberto e não pode ter fins comerciais.
Mais informações: https://www.gnu.org/licenses/agpl-3.0.html
"""

import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)

def fetch_questions(theme_id=None):
    base_query = '''
        SELECT question_text, option_1, option_2, correct_answer
        FROM questions
    '''
    if theme_id is not None:
        base_query += " WHERE theme_id = %s"
    base_query += " ORDER BY RAND() LIMIT 50"

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                if theme_id is not None:
                    cursor.execute(base_query, (theme_id,))
                else:
                    cursor.execute(base_query)
                rows = cursor.fetchall()
                return [
                    {
                        "question": row["question_text"],
                        "options": [row["option_1"], row["option_2"]],
                        "answer": row["correct_answer"],
                    }
                    for row in rows
                ]
    except Exception as e:
        print("Erro ao buscar perguntas:", e)
        return []


def insert_question(question_data, theme_id=1):
    """
    Insere uma nova pergunta no banco de dados, validando duplicidade via campo `source`.
    """
    question_text, option_1, option_2, correct_answer, source = question_data

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 FROM questions WHERE source = %s", (source,))
                if cursor.fetchone():
                    print(f"🔁 Pergunta já existe no banco: {source}")
                    return

                cursor.execute(
                    """
                    INSERT INTO questions (question_text, option_1, option_2, correct_answer, source, theme_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (question_text, option_1, option_2, correct_answer, source, theme_id)
                )
                conn.commit()
                print(f"✅ Pergunta inserida: {source}")
    except Exception as e:
        print("❌ Erro ao inserir pergunta:", e)
