# -*- coding: UTF-8 -*-
# encoding=utf8

import db.tokens as tk
from funcs import *
import telebot
from telebot import *
import requests

img_url = "https://image.tmdb.org/t/p/w500"

tb = telebot.TeleBot(tk.TOKEN)
user = tb.get_me()

def extract_arg(arg):
    return arg.split(" ", 1)[1:]



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
    pass

@tb.message_handler(commands=['search'])
def search(m):
    q = extract_arg(m.text)
    qr = ""
    for w in q:
        qr += w + " " 
    t = searchFilm(tb, tk.API_KEY_TMDB, qr)
    tb.send_message(m.chat.id, t, parse_mode="Markdown")
    print(user)

tb.polling()
