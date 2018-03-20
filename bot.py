# -*- coding: UTF-8 -*-
# encoding=utf8

import db.tokens as tk
from funcs import *
import math
import telebot
from telebot import *
import requests
from db.db import *

import sys
reload(sys)
sys.setdefaultencoding('UTF8')

img_url = "https://image.tmdb.org/t/p/w500"
conn = sqlite3.connect('db/users.db', check_same_thread = False)
c = conn.cursor()
#c.execute("""CREATE TABLE IF NOT EXISTS  movie_user (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, movie TEXT, estado INTEGER)""")

tb = telebot.TeleBot(tk.TOKEN)



################################################
#################### INLINE ####################
################################################

@tb.inline_handler(lambda query: query.query.lower() == 'help' or query.query == '' )
def inline_help(q):
    inline = types.InlineQueryResultArticle(1,
                                            "AYUDA",
                                            types.InputTextMessageContent("/help", parse_mode="Markdown"),
                                            description="Muestra ayuda sobre las consultas posibles al bot",
                                            thumb_url='http://dev.dsgdsr.me/botcine/help.jpg')
    tb.answer_inline_query(q.id, [inline], cache_time=1)

@tb.inline_handler(lambda query: (query.query.startswith('cartelera') or query.query.startswith('now_palying') or query.query.startswith('encines'))
                   and len(query.query.split()) == 1)
def inline_cartelera(q):
    sendInlineQuery(tb, q.id, img_url, tk.API_KEY_TMDB, "now_playing", 20)

@tb.inline_handler(lambda query: (query.query.startswith('upcoming') or query.query.startswith('featured') or query.query.startswith('porvenir') or query.query.startswith('proximamente'))
                   and len(query.query.split()) == 1)
def inline_upcoming(q):
    sendInlineQuery(tb, q.id, img_url, tk.API_KEY_TMDB, "upcoming", 10)

@tb.inline_handler(lambda query: (query.query.startswith('top') or query.query.startswith('valoradas'))
                   and len(query.query.split()) == 1)
def inline_top(q):
    sendInlineQuery(tb, q.id, img_url, tk.API_KEY_TMDB, "top_rated", 20)

@tb.inline_handler(lambda query: (query.query.startswith('populares') or query.query.startswith('popu') or query.query.startswith('pop'))
                   and len(query.query.split()) == 1)
def inline_popu(q):
    sendInlineQuery(tb, q.id, img_url, tk.API_KEY_TMDB, "popular", 20)

@tb.inline_handler(lambda query: True)
def inline_handler(q):
    sendInlineSearch(tb, q.id, img_url, tk.API_KEY_TMDB, q.query, 10)



##################################################
#################### COMANDOS ####################
##################################################

@tb.message_handler(commands=['start'])
def welcome(m):
    tb.send_message(m.chat.id, "Bienvenido "+m.from_user.first_name+". \n Disfruta del bot, si necesitas ayuda haz uso del comando '/help'.")

@tb.message_handler(commands=['help'])
def help(m):
    presentacion = "*Ayuda* \nLos comandos In-Line no deben enviarse, sólo colocarlos en la línea de texto. \n"
    comandos = "Aquí se exponen todos los comandos: \n=> upcoming - devuelve un listado con las películas a estrenar \n=> valoradas - devuelve un listado con las películas más valoradas \n=> populares - devuelve un listado con las películas populares del momento.\n=> cartelera - devuelve un listado con las películas actualmente en los cines.\nSi sólo se escribe el nombre de la película, se hará una búsqueda de ella.\n\n"
    spam = "Bot creado por @Skr0tex, @andresitoperson y @davidsnchz99"
    txt = presentacion + comandos + spam
    tb.send_message(m.chat.id, txt, parse_mode="Markdown")

@tb.message_handler(commands=['cartelera'])
def cartelera(m):
    cart = searchSec(tb, tk.API_KEY_TMDB, "now_playing")
    t = cart[0]
    img = cart[1]
    tb.send_photo(m.chat.id, img)
    tb.send_message(m.chat.id, t, parse_mode="Markdown")

@tb.message_handler(commands=['search'])
def search(m):
    q = extract_arg(m.text)
    qr = ""
    for w in q:
        qr += w + " "
    t = searchFilm(tb, tk.API_KEY_TMDB, qr)
    tb.send_message(m.chat.id, t, parse_mode="Markdown")

@tb.message_handler(commands=['lista'])
def lista(m):   
    lista = getMovies(m.from_user.id, conn, c)
    num = len(lista)
    pages = int(math.ceil(num/10.0))
    keyboard = []
    for p in range(pages):
        keyboard.append([types.InlineKeyboardButton(text=p+1, callback_data='page')])
    print(keyboard)
    tb.send_message(m.chat.id, "hola", reply_markup=types.InlineKeyboardMarkup(keyboard))

@tb.message_handler(commands=['movie'])
def movie(m):
    q = extract_arg(m.text)
    qr = ""
    for w in q:
        qr += w + " "
    t = getMovieInfo(tb, tk.API_KEY_TMDB, qr, m.chat.id, conn, c) #337167
    tb.send_photo(m.chat.id, t[1])
    tb.send_message(m.chat.id, t[0], parse_mode="Markdown", reply_markup=t[2])



###################################################
#################### CALLBACKS ####################
###################################################

@tb.callback_query_handler(func=lambda call: call.data.startswith('add_pend'))
def add_pend_handler(call):
    idu = call.from_user.id
    idp = extract_arg(call.data)
    addM = addMovie(idu, idp[0], pend, conn, c)
    if(addM == None):
        tb.send_message(call.from_user.id, "La película ya esta en tu lista de pendientes", parse_mode="Markdown")
    else:
        tb.send_message(call.from_user.id, "Película añadida a pendientes", parse_mode="Markdown")

@tb.callback_query_handler(func=lambda call: call.data.startswith('add_seen'))
def add_pend_handler(call):
    idu = call.from_user.id
    idp = extract_arg(call.data)
    addM = addMovie(idu, idp[0], seen, conn, c)
    if(addM == None):
        tb.send_message(call.from_user.id, "La película ya esta en tu lista de vistas", parse_mode="Markdown")
    else:
        tb.send_message(call.from_user.id, "Película añadida a vistas", parse_mode="Markdown")

@tb.callback_query_handler(func=lambda call: call.data.startswith('set_seen'))
def add_pend_handler(call):
    idu = call.from_user.id
    idp = extract_arg(call.data)
    setM = setMovie(idu, idp[0], seen, conn, c)
    if(setM == None):        
        tb.send_message(call.from_user.id, "Error: la película no esta en tu lista de pendientes; Pruebe a ejecutar el comando /movie " + str(idp[0]) + " y añadirla a vistas", parse_mode="Markdown")
    elif(setM == 1):
        tb.send_message(call.from_user.id, "Película añadida a vistas", parse_mode="Markdown")
    elif(setM == 0):
        tb.send_message(call.from_user.id, "La película ya esta en tu lista de vistas", parse_mode="Markdown")

@tb.callback_query_handler(func=lambda call: call.data.startswith('del_movie'))
def add_pend_handler(call):
    idu = call.from_user.id
    idp = extract_arg(call.data)
    delM = delMovie(idu, idp[0], conn, c)
    if(delM == None):
        tb.send_message(call.from_user.id, "Error: La película no se encuentra en tu lista", parse_mode="Markdown")
    else:
        tb.send_message(call.from_user.id, "Película eliminada de la lista!", parse_mode="Markdown")

tb.polling()
