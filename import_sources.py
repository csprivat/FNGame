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

import csv
from db import get_connection

def insert_source(cursor, url, title, description):
    query = """
    INSERT INTO sources (url, title, description)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE title = VALUES(title), description = VALUES(description)
    """
    cursor.execute(query, (url, title, description))

def main():
    with open("fontes.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

    conn = get_connection()
    cursor = conn.cursor()

    for row in data:
        insert_source(cursor, row["url"], row["title"], row["description"])

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Fontes importadas com sucesso.")

if __name__ == "__main__":
    main()
