from bot import telebot, tb, os, implist

implist.append(os.path.basename(__file__))

@tb.message_handler(commands=['start'])
def welcome(m):
    tb.send_message(m.chat.id, "Bienvenido "+m.from_user.first_name+". \n Disfruta del bot, si necesitas ayuda haz uso del comando '/help'.")
