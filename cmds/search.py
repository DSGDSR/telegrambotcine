from bot import telebot, tb, os, implist, API_KEY_TMDB, requests, img_url, conn, c, math
from extra.funcs import *
from telebot import *

implist.append(os.path.basename(__file__))

@tb.message_handler(commands=['search', 'buscar'])
def search(m):
    q = extract_arg(m.text)
    qr = ""
    for w in q:
        qr += w + " "
    t = searchFilm(tb, API_KEY_TMDB, qr)
    tb.send_message(m.chat.id, t, parse_mode="Markdown")