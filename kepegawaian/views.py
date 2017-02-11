import telebot

API_TOKEN = '321364862:AAFE6CglJ_u8-TGuAbV7YBIiIU0rhqukNTI'

bot = telebot.TeleBot(API_TOKEN)

def kirim_notifikasi_telegram(chat_id, pesan):
    bot.send_message(chat_id, pesan)
    return True