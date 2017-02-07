

import telebot
from telebot import types

TOKEN = '321364862:AAFE6CglJ_u8-TGuAbV7YBIiIU0rhqukNTI'

commands = {  # command description used in the "help" command
              'start': 'Untuk menggunakan Bot',
              'bantuan': 'Memberikan anda informasi tetang perintah yang tersedia',
              'daftar': 'Mendaftarkan ID anda kedalam aplikasi SIMPATIK',
}


# error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print "New user detected, who hasn't used \"/start\" yet"
        return 0


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener

# bantuan page
@bot.message_handler(commands=['start'])
def command_help(m):
    cid = m.chat.id
    help_text = "Selamat Datang, Simpatik Bot ini hanya untuk notifikasi aplikasi SIMPATIK kab. Kediri\n"
    help_text += "Perintah yang tersedia : \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page

# bantuan page
@bot.message_handler(commands=['bantuan'])
def command_help(m):
    cid = m.chat.id
    help_text = "Perintah yang tersedia : \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page


user_dict = {}

class User:
    def __init__(self, nip):
        self.nip = nip

@bot.message_handler(commands=['daftar'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Selamat datang, Pendaftaran Step 1.
Silahkan masukkan NIP/NIK anda
""")
    bot.register_next_step_handler(msg, process_verify_step)

def process_verify_step(message):
    try:
        chat_id = message.chat.id
        nip = message.text
        if not nip.isdigit():
            msg = bot.reply_to(message, 'NIP/NIK harus angka, Silahkan masukkan NIP/NIK anda')
            bot.register_next_step_handler(msg, process_verify_step)
            return
        # cek didatabase berdasarkan NIP/NIK
        # Jika tidak ada kembali inputan NIP
        user = User(nip)
        user_dict[chat_id] = user
        text = 'NIP/NIK ditemukan, \n'
        text += 'dengan Nama '+nip+' \n'
        text += 'Silahkan klik tautan berikut http://127.0.0.1:8000/admin untuk verifikasi'
        bot.reply_to(message, text)
    except Exception as e:
        bot.reply_to(message, e)

bot.polling()