import telebot
from django.conf import settings 

# API_TOKEN = '321364862:AAFE6CglJ_u8-TGuAbV7YBIiIU0rhqukNTI'
API_TOKEN = settings.TELGRAM_API_TOKEN

bot = telebot.TeleBot(API_TOKEN)

def kirim_notifikasi_telegram(chat_id, pesan):
    bot.send_message(chat_id, pesan)
    return True