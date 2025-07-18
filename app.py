import os
import telebot
from flask import Flask, request
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests

load_dotenv()

# Configurações do bot
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Configurações do Spotify
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")

# Inicializa o Flask
app = Flask(__name__)

# Comando /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bem vindo ao Vampirizer!\n\nComandos:\n/reglast <seu_user_lastfm>\n/regspotify\n/vampirizar <vitima_lastfm>")

# Comando /reglast
@bot.message_handler(commands=['reglast'])
def reglast(message):
    user_lastfm = message.text.split()[1]
    # Aqui você deve adicionar a lógica para registrar o usuário no Last.fm
    bot.reply_to(message, f"Usuário Last.fm {user_lastfm} registrado!")

# Comando /regspotify
@bot.message_handler(commands=['regspotify'])
def regspotify(message):
    # Aqui você deve gerar o link de autenticação do Spotify
    sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
    auth_url = sp_oauth.get_authorize_url()
    bot.reply_to(message, f"Conecte seu Spotify aqui: {auth_url}")

# Comando /vampirizar
@bot.message_handler(commands=['vampirizar'])
def vampirizar(message):
    vitima_lastfm = message.text.split()[1]
    # Aqui você deve adicionar a lógica para "vampirizar" a música da vítima
    bot.reply_to(message, f"Vampirizando {vitima_lastfm}!")

# Webhook para receber atualizações do Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.get_json())
    bot.process_new_updates([update])
    return 'OK', 200

# Inicia o Flask na porta 8080
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
