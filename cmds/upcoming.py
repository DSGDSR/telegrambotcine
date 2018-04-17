from bot import telebot, tb, os, implist, API_KEY_TMDB, requests, img_url, conn, c, math
from extra.funcs import *

implist.append(os.path.basename(__file__))

@tb.message_handler(commands=['upcoming', 'proximamente'])
def cartelera(m):
    cart = searchSec(tb, API_KEY_TMDB, "upcoming")
    t = cart[0]
    img = cart[1]
    tb.send_photo(m.chat.id, img)
    tb.send_message(m.chat.id, t, parse_mode="Markdown")