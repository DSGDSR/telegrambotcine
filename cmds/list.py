from bot import telebot, tb, os, implist, conn, c, math
from extra.funcs import *

implist.append(os.path.basename(__file__))

@tb.message_handler(commands=['lista'])
def lista(m):   
    lista = getMovies(m.from_user.id, conn, c)
    num = len(lista)
    pages = int(math.ceil(num/10.0))
    kbb = types.InlineKeyboardMarkup(6)
    kb = types.InlineKeyboardMarkup(4)

markup = types.ReplyKeyboardMarkup()
    kbb.add(types.InlineKeyboardButton('1', callback_data='movie ' + ))
    kb.add(types.InlineKeyboardButton('⏪', callback_data='first '),
           types.InlineKeyboardButton('⬅', callback_data='prev '),
           types.InlineKeyboardButton('➡', callback_data='next '),
           types.InlineKeyboardButton('⏩', callback_data='last '))
    tb.send_message(m.chat.id, "hola", reply_markup=kb)