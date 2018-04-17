from bot import telebot, tb, os, implist, API_KEY_TMDB, requests, img_url, conn, c, math
from extra.funcs import *
from telebot import *

implist.append(os.path.basename(__file__))

@tb.message_handler(commands=['movie', 'film', 'pelicula', 'peli'])
def movie(m):
    q = extract_arg(m.text)
    qr = ""
    for w in q:
        qr += w + " "
    t = getMovieInfo(tb, API_KEY_TMDB, qr, m.chat.id, conn, c) #337167
    #tb.send_photo(m.chat.id, t[1])
    tb.send_message(m.chat.id, t[0], parse_mode="Markdown", reply_markup=t[2])