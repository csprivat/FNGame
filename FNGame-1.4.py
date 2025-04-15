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
import random
import telebot
from dotenv import load_dotenv
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from db import get_connection, fetch_questions

load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")
if not token:
    raise ValueError("Token TELEGRAM_BOT_TOKEN nao definido no .env")

bot = telebot.TeleBot(token)

MAX_QUESTIONS_PER_SESSION = 10
user_progress = {}
user_scores = {}
user_sessions = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        (
            "🧠 Bem-vindo ao Quiz Anti Fake News!\n\n"
            "📋 Instrucoes:\n"
            "1. Escolha um tema com /temas\n"
            f"2. Voce respondera {MAX_QUESTIONS_PER_SESSION} perguntas\n"
            "3. Use os botoes para responder\n\n"
            "Comandos disponiveis:\n"
            "/temas - Escolher tema\n"
            "/pontuacao - Ver sua pontuacao\n"
            "/reiniciar - Recomecar quiz atual\n"
            "/ranking - Ranking dos jogadores\n"
            "/about - Sobre o projeto"
        )
    )

@bot.message_handler(commands=['temas'])
def listar_temas(message):
    chat_id = message.chat.id
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, title FROM themes ORDER BY id")
                temas = cursor.fetchall()
    except Exception as e:
        bot.send_message(chat_id, "⚠️ Erro ao buscar temas.")
        print("Erro ao buscar temas:", e)
        return

    if not temas:
        bot.send_message(chat_id, "❌ Nenhum tema disponivel.")
        return

    markup = InlineKeyboardMarkup()
    for tema in temas:
        markup.add(InlineKeyboardButton(tema['title'], callback_data=f"tema_{tema['id']}"))

    bot.send_message(chat_id, "🧠 Escolha um tema para comecar o quiz:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("tema_"))
def iniciar_quiz_por_tema(call):
    chat_id = call.message.chat.id
    theme_id = int(call.data.split("_")[1])

    try:
        questions = fetch_questions(theme_id=theme_id)
    except Exception as e:
        bot.send_message(chat_id, "⚠️ Erro ao iniciar quiz. Tente novamente.")
        print("Erro ao buscar perguntas:", e)
        return

    if not questions:
        bot.send_message(chat_id, "❌ Nenhuma pergunta encontrada para este tema.")
        return

    random.shuffle(questions)
    user_progress[chat_id] = 0
    user_scores[chat_id] = 0
    user_sessions[chat_id] = {
        "questions": questions[:MAX_QUESTIONS_PER_SESSION],
        "theme_id": theme_id,
    }

    bot.send_message(chat_id, "✅ Tema selecionado! Vamos comecar!")
    send_question(chat_id)

@bot.message_handler(commands=['about'])
def about_command(message):
    bot.send_message(
        message.chat.id,
        "ℹ️ Este quiz e uma iniciativa para combater a desinformacao.\n\n"
        "Baseado em noticias reais e boatos populares.\n"
        "Criado para promover o pensamento critico e o consumo consciente de informacao.\n"
    )

@bot.message_handler(commands=['pontuacao'])
def show_score(message):
    chat_id = message.chat.id
    score = user_scores.get(chat_id, 0)
    progress = user_progress.get(chat_id, 0)
    bot.send_message(chat_id, f"📊 Sua pontuacao atual: {score}/{progress}")

@bot.message_handler(commands=['reiniciar'])
def restart_quiz(message):
    chat_id = message.chat.id
    session = user_sessions.get(chat_id)
    if not session:
        bot.send_message(chat_id, "❌ Nenhum quiz ativo. Use /temas para comecar.")
        return

    theme_id = session.get("theme_id")
    try:
        questions = fetch_questions(theme_id=theme_id)
    except Exception as e:
        bot.send_message(chat_id, "⚠️ Erro ao reiniciar quiz. Tente novamente.")
        print("Erro ao reiniciar quiz:", e)
        return

    random.shuffle(questions)
    user_scores[chat_id] = 0
    user_progress[chat_id] = 0
    user_sessions[chat_id] = {
        "questions": questions[:MAX_QUESTIONS_PER_SESSION],
        "theme_id": theme_id,
    }
    bot.send_message(chat_id, "🔄 O quiz foi reiniciado!")
    send_question(chat_id)

def send_question(chat_id):
    index = user_progress.get(chat_id, 0)
    session = user_sessions.get(chat_id, {})
    session_questions = session.get("questions", [])
    if index < len(session_questions):
        q = session_questions[index]
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        for opt in q["options"]:
            markup.add(opt)
        bot.send_message(chat_id, q["question"], reply_markup=markup)
    else:
        show_results(chat_id)

def salvar_pontuacao_total(chat_id):
    score = user_scores.get(chat_id, 0)

    try:
        chat = bot.get_chat(chat_id)
        username = chat.username if chat.username else "desconhecido"
    except Exception as e:
        print(f"❌ Erro ao obter username para chat_id {chat_id}: {e}")
        username = "erro_username"

    print(f"📥 Salvando pontuação: chat_id={chat_id}, username={username}, score={score}")

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT score FROM user_scores WHERE telegram_user_id = %s", (chat_id,))
                result = cursor.fetchone()

                if result:
                    cursor.execute(
                        "UPDATE user_scores SET score = score + %s, last_played = NOW() WHERE telegram_user_id = %s",
                        (score, chat_id)
                    )
                    print("🔁 Score atualizado com sucesso.")
                else:
                    cursor.execute(
                        "INSERT INTO user_scores (telegram_user_id, username, score) VALUES (%s, %s, %s)",
                        (chat_id, username, score)
                    )
                    print("✅ Novo score inserido com sucesso.")

                conn.commit()
    except Exception as e:
        print(f"❌ Erro ao salvar pontuação no banco para {chat_id}: {e}")

def send_feedback(chat_id, score):
    if score <= 2:
        msg = (
            "⚠️ Você ainda está aprendendo a identificar notícias falsas, e isso é totalmente normal!\n\n"
            "👉 Que tal começar conhecendo o Guia da SaferNet sobre fake news?\n"
            "🔗 https://www.safernet.org.br/site/prevencao/fake-news\n\n"
            "🧠 Também recomendamos a Cartilha do CERT-BR sobre boatos:\n"
            "🔗 https://cartilha.cert.br/fasciculos/boatos/fasciculo-boatos.pdf\n\n"
            "📚 Aprender a checar informações é um superpoder! 💪"
        )
    elif score <= 4:
        msg = (
            "🔍 Você já sabe algumas coisas sobre fake news. Ótimo começo!\n\n"
            "📘 Quer aprender ainda mais? Dá uma olhada nestes sites:\n"
            "• Projeto Comprova: https://projetocomprova.com.br/\n"
            "• Cartilha do CERT-BR: https://cartilha.cert.br/fasciculos/boatos/fasciculo-boatos.pdf\n\n"
            "💡 Continue praticando, você está no caminho certo!"
        )
    elif score <= 7:
        msg = (
            "✅ Muito bem! Você já entende sobre o que é uma fake news.\n\n"
            "Continue praticando e ajude seus amigos e familiares a ficarem bem informados também! 💬🧠"
        )
    elif score <= 9:
        msg = (
            "🎯 Mandou muito bem! Você acertou quase tudo!\n\n"
            "👏 Parabéns por saber identificar boatos e notícias falsas.\n"
            "👥 Que tal ajudar outras pessoas a fazerem o mesmo?"
        )
    else:
        msg = (
            "🏆 Nota 10! Você gabaritou o quiz! 🔥\n\n"
            "Você mostrou que entende muito bem como se proteger das fake news.\n"
            "👏 Continue espalhando informação de verdade!"
        )
    bot.send_message(chat_id, msg)

def show_results(chat_id):
    score = user_scores[chat_id]
    total = len(user_sessions.get(chat_id, {}).get("questions", []))
    bot.send_message(
        chat_id,
        f"🎉 Quiz completo! Sua pontuacao: {score}/{total}",
        reply_markup=ReplyKeyboardRemove()
    )
    salvar_pontuacao_total(chat_id)
    send_feedback(chat_id, score)

@bot.message_handler(func=lambda message: message.chat.id in user_progress and not message.text.startswith("/"))
def handle_answer(message):
    chat_id = message.chat.id
    index = user_progress.get(chat_id, 0)
    session = user_sessions.get(chat_id, {})
    session_questions = session.get("questions", [])
    if index >= len(session_questions):
        bot.send_message(chat_id, "✅ Voce ja completou o quiz. Use /temas para jogar novamente.")
        return

    selected = message.text
    current_q = session_questions[index]
    correct = current_q["answer"]
    options = current_q["options"]

    if selected not in options:
        bot.send_message(chat_id, "⚠️ Resposta invalida. Use os botoes para responder.")
        return

    if selected == correct:
        user_scores[chat_id] += 1
        bot.send_message(chat_id, "✅ Resposta correta!")
    else:
        bot.send_message(chat_id, f"❌ Resposta incorreta.\nCorreto: {correct}")

    user_progress[chat_id] += 1
    send_question(chat_id)


@bot.message_handler(commands=['ranking'])
def mostrar_ranking(message):
    chat_id = message.chat.id
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT username, score FROM user_scores ORDER BY score DESC LIMIT 5")
                top_users = cursor.fetchall()

        if not top_users:
            bot.send_message(chat_id, "📊 Ainda não há pontuações registradas.")
            return

        msg = "🏆 Ranking dos Participantes:"
        for idx, user in enumerate(top_users, start=1):
            username = user["username"] or "desconhecido"
            msg += f"{idx}️⃣ @{username} - {user['score']} pontos"
        msg += "📊 Continue jogando para subir no ranking!"
        bot.send_message(chat_id, msg)

    except Exception as e:
        print("⚠️ Erro ao acessar o ranking:", e)
        bot.send_message(chat_id, "⚠️ Ranking indisponível no momento. Tente novamente mais tarde.")
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT username, score FROM user_scores ORDER BY score DESC LIMIT 5")
                top_users = cursor.fetchall()
                if not top_users:
                    bot.send_message(chat_id, "📊 Ainda nao ha pontuacoes registradas.")
                    return
                msg = "🏆 Ranking dos Participantes:\n\n"
                for idx, user in enumerate(top_users, start=1):
                    username = user['username'] or 'desconhecido'
                    msg += f"{idx}️⃣ @{username} - {user['score']} pontos\n"
                msg += "\n📊 Continue jogando para subir no ranking!"
                bot.send_message(chat_id, msg)
    except Exception as e:
        bot.send_message(chat_id, "⚠️ Erro ao acessar o ranking. Tente novamente.")
        print("Erro ao gerar ranking:", e)

bot.infinity_polling(timeout=10, long_polling_timeout=5)