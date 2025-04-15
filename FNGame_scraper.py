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

import requests
from bs4 import BeautifulSoup
import mysql.connector
import os
from dotenv import load_dotenv
from db import insert_question

# Carrega variáveis de ambiente do .env
load_dotenv()

DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'port': int(os.getenv("DB_PORT", 3306)),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME"),
}

BASE_URL = 'https://www.boatos.org/'

def coletar_links(limit=10):
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        print("❌ Erro ao acessar a página principal:", response.status_code)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    artigos = soup.find_all('h2', class_='entry-title', limit=limit)
    links = [artigo.find('a')['href'] for artigo in artigos if artigo.find('a')]
    return links

def extrair_informacoes(link):
    response = requests.get(link)
    if response.status_code != 200:
        print(f"❌ Erro ao acessar {link}: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    titulo_tag = soup.find('h1', class_='entry-title')
    conteudo_tag = soup.find('div', class_='entry-content')

    titulo = titulo_tag.text.strip() if titulo_tag else "Sem título"
    conteudo = conteudo_tag.text.strip() if conteudo_tag else "Sem conteúdo"

    pergunta = f"Notícia: '{titulo}'. Isso é verdadeiro ou falso?"

    return (pergunta, "Verdadeiro", "Falso", "Falso", link)


if __name__ == "__main__":
    theme_id = 1  # <<<< ALTERE AQUI O ID DO TEMA
    print(f"🔎 Coletando artigos do Boatos.org para o tema ID {theme_id}...")
    links = coletar_links(limit=10)
    print(f"🔗 {len(links)} artigos encontrados.")

    perguntas = []
    for link in links:
        info = extrair_informacoes(link)
        if info:
            perguntas.append(info)

    print(f"✅ {len(perguntas)} perguntas extraídas.")
    for p in perguntas:
        insert_question(p, theme_id=theme_id)
    print("📥 Perguntas inseridas no banco com sucesso.")
