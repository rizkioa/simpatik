import telebot

TOKEN = '321364862:AAFE6CglJ_u8-TGuAbV7YBIiIU0rhqukNTI'

commands = {  # command description used in the "help" command
              'start': 'Get used to the bot',
              'help': 'Gives you information about the available commands',
              'sendLongText': 'A test using the \'send_chat_action\' command',
              'getImage': 'A test using multi-stage messages, custom keyboard, and media sending'
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


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    # bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")
    bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")

bot.polling()