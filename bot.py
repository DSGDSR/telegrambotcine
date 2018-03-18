# -*- coding: UTF-8 -*-
# encoding=utf8

import db.tokens as tk
from funcs import *
import telebot
from telebot import *
import requests

img_url = "https://image.tmdb.org/t/p/w500"

tb = telebot.TeleBot(tk.TOKEN)

def extract_arg(arg):
    return arg.split(" ", 1)[1:]

@tb.inline_handler(lambda query: True)
def inline_handler(q):
    opt = q.query.split(" ", 1)[0].strip(" ")
    #print(opt)
    if opt=="valoradas":
        sendInlineQuery(tb, q.id, img_url, tk.API_KEY_TMDB, "top_rated", 20)

    elif opt=="populares":
        sendInlineQuery(tb, q.id, img_url, tk.API_KEY_TMDB, "popular", 20)

    elif opt=="upcoming":
        sendInlineQuery(tb, q.id, img_url, tk.API_KEY_TMDB, "upcoming", 10)

    elif opt=="cartelera":
        sendInlineQuery(tb, q.id, img_url, tk.API_KEY_TMDB, "now_playing", 20)

    else:
        sendInlineSearch(tb, q.id, img_url, tk.API_KEY_TMDB, q.query, 10)

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
    sendInlineQuery(tb, m.from_user.id, img_url, tk.API_KEY_TMDB, "now_playing", 20)

@tb.message_handler(commands=['search'])
def search(m):
    q = extract_arg(m.text)
    t = searchFilm(tb, tk.API_KEY_TMDB, q)
    tb.send_message(m.chat.id, t, parse_mode="Markdown")

tb.polling()

'''@tb.message_handler(commands=['search'])
def search(m):
    search = tmdb.Search()
    q = extract_arg(m.text)
    resp = search.movie(query=q)
    #tb.send_message(m.from_user.id, q)
    #print(search.results)
    for f in search.results[:5]:
        print(f['title'])

@tb.message_handler(commands=['cartelera'])
def search(m):
    url = "https://api.themoviedb.org/3/movie/now_playing?api_key=" + tmdb_key
    response = requests.get(url)
    data = response.json()['results']
    #print(response.json())
    for f in data[:20]:
        print(f['title'])

@tb.message_handler(commands=["upcoming"])
def print_upcoming(m):
    url = "https://api.themoviedb.org/3/movie/upcoming?language=es-ES&api_key=" + tk.API_KEY_TMDB
    response = requests.get(url)
    for i in response.json()["results"]:
        bot.send_message(m.chat.id, i["title"])'''
