# -*- coding: utf-8 -*-
"""
FNGame_scraper.py
Script para coletar perguntas automaticamente e classificá-las por tema com base em palavras-chave.
Licença: AGPLv3
"""

import requests
from bs4 import BeautifulSoup
import mysql.connector
import os
from dotenv import load_dotenv
from db import insert_question
from classifier import classificar_categoria_por_keywords
from category_keywords import DICIONARIO_TEMAS

# Carrega variáveis de ambiente do .env
load_dotenv()

DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'port': int(os.getenv("DB_PORT", 3306)),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME"),
}

BASE_URL = 'https://www.boatos.org/brasil'

MAPEAMENTO_CATEGORIA_THEME_ID = {
    "Política": 2,
    "Saúde": 3,
    "Tecnologia": 4,
    "Educação": 1,
    "Meio Ambiente": 4,
}

def coletar_links(limit=30):
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
    print("🔎 Coletando artigos do Boatos.org...")
    links = coletar_links(limit=30)
    print(f"🔗 {len(links)} artigos encontrados.")

    perguntas = []
    for link in links:
        info = extrair_informacoes(link)
        if info:
            perguntas.append(info)

    print(f"✅ {len(perguntas)} perguntas extraídas.")

    for p in perguntas:
        pergunta_texto = p[0]
        categoria = classificar_categoria_por_keywords(pergunta_texto, DICIONARIO_TEMAS)
        theme_id_classificado = MAPEAMENTO_CATEGORIA_THEME_ID.get(categoria, 1)
        pergunta_com_categoria = list(p)
        pergunta_com_categoria.insert(4, categoria)  # Insere 'category' antes do 'source'
        insert_question(tuple(pergunta_com_categoria), theme_id=theme_id_classificado)
        print(f"📌 Classificada como '{categoria or 'Desconhecida'}' (theme_id={theme_id_classificado})")
    print("📥 Perguntas inseridas com sucesso no banco.")
