# -*- coding: UTF-8 -*-
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#users = {}

import telebot
from telebot import *
import tmdbsimple as tmdb
from tokens import *
import requests

img_url = "https://image.tmdb.org/t/p/w500"
tmdb.API_KEY = API_KEY_TMDB

tb = telebot.TeleBot(TOKEN)

'''def addFilm(idu, idp):
    if idu in users:
        users[idu].append(idp)
    else:
        users[idu] = [idp]

def removeFilm(idu, idp):
    users[idu].remove(idp)'''

def extract_arg(arg):
    return arg.split(" ", 1)[1:]

@tb.message_handler(commands=['start'])
def welcome(q):
    tb.send_message(q.chat.id, "Bienvenido "+q.from_user.first_name+". \n Disfruta del bot, si necesitas ayuda haz uso del comando '/help'.")

@tb.message_handler(commands=['help'])
def help(q):
    presentacion = "*Ayuda* \nLos comandos In-Line no deben enviarse, sólo colocarlos en la línea de texto. \n"
    comandos = "Aquí se exponen todos los comandos: \n=> upcoming - devuelve un listado con las películas a estrenar \n=> valoradas - devuelve un listado con las películas más valoradas \n=> populares - devuelve un listado con las películas populares del momento.\n=> cartelera - devuelve un listado con las películas actualmente en los cines.\nSi sólo se escribe el nombre de la película, se hará una búsqueda de ella.\n\n"
    spam = "Bot creado por @Skr0tex, @andresitoperson y @davidsnchz99"
    aux = presentacion + comandos + spam
    tb.send_message(q.chat.id, aux, parse_mode="Markdown")

@tb.inline_handler(lambda query: True)
def search(q):
    opt = q.query.split(" ", 1)[0].strip(" ")
    #print(opt)
    if opt=="valoradas":
        #try:
            list = []
            i = 1
            url_foto = 'https://image.tmdb.org/t/p/w500'
            url = "https://api.themoviedb.org/3/movie/top_rated?language=es-ES&api_key=" + API_KEY_TMDB
            response = requests.get(url)
            data = response.json()['results']
            id = 1
            for i in data[:20]:
                list.append(types.InlineQueryResultArticle(id, i['title'], types.InputTextMessageContent("[⁣]("+ url_foto+i['backdrop_path'] + ")"+"\n"+'*'+i['title']+'*'+'\n\n'+i['overview'], parse_mode="Markdown"),description=i['overview'],thumb_url=url_foto+i['backdrop_path'],hide_url=True))
                id+=1

            tb.answer_inline_query(q.id, list, cache_time=1)
        #except:
            pass

    if opt=="populares":
        #try:
            list = []
            i = 1
            url_foto = 'https://image.tmdb.org/t/p/w500'
            url = "https://api.themoviedb.org/3/movie/popular?language=es-ES&api_key=" + API_KEY_TMDB
            response = requests.get(url)
            data = response.json()['results']
            id = 1
            for i in data[:20]:
                list.append(types.InlineQueryResultArticle(id,i['title'],types.InputTextMessageContent("[⁣]("+ url_foto+i['backdrop_path'] + ")"+"\n"+'*'+i['title']+'*'+'\n\n'+i['overview'], parse_mode="Markdown"),description=i['overview'],thumb_url=url_foto+i['backdrop_path'],hide_url=True))
                id+=1

            tb.answer_inline_query(q.id, list, cache_time=1)
        #except:
            pass

    if opt=="upcoming":
        try:
            list = []
            i = 1
            url_foto = 'https://image.tmdb.org/t/p/w500'
            url = "https://api.themoviedb.org/3/movie/upcoming?language=es-ES&api_key=" + API_KEY_TMDB
            response = requests.get(url)
            id = 1
            for i in response.json()['results']:
                list.append(types.InlineQueryResultArticle(id,i['title'],types.InputTextMessageContent("[⁣]("+ url_foto+i['backdrop_path'] + ")"+"\n"+'*'+i['title']+'*'+'\n\n'+i['overview'], parse_mode="Markdown"),description=i['overview'],thumb_url=url_foto+i['backdrop_path'],hide_url=True))
                id+=1

            tb.answer_inline_query(q.id, list, cache_time=1)
        except:
            pass

    if opt=="cartelera":
        try:
            url = "https://api.themoviedb.org/3/movie/now_playing?language=es-ES&api_key=" + API_KEY_TMDB
            response = requests.get(url)
            data = response.json()['results']
            lista_query = []
            i = 1
            for f in data[:20]:
                lista_query.append(types.InlineQueryResultArticle(i,f['title'],types.InputTextMessageContent("[⁣]("+ img_url+f['backdrop_path'] + ")"+"\n"+'*'+f['title']+'*'+'\n\n'+f['overview'], parse_mode="Markdown"),description=f['overview'],thumb_url=img_url+f['backdrop_path']))
                i+=1
            tb.answer_inline_query(q.id, lista_query, cache_time=1)
        except:
            pass

    else:
        try:
            search = tmdb.Search()
            resp = search.movie(query=q.query)
            lista_query = []
            i = 1
            for f in search.results[:10]:
                lista_query.append(types.InlineQueryResultArticle(i,f['title'],types.InputTextMessageContent("[⁣]("+ img_url+f['backdrop_path'] + ")"+"\n"+'*'+f['title']+'*'+'\n\n'+f['overview'], parse_mode="Markdown"),description=f['overview'],thumb_url=img_url+f['backdrop_path']))
                i+=1

            tb.answer_inline_query(q.id, lista_query, cache_time=1)
        except:
            pass

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
    url = "https://api.themoviedb.org/3/movie/upcoming?language=es-ES&api_key=" + API_KEY_TMDB
    response = requests.get(url)
    for i in response.json()["results"]:
        bot.send_message(m.chat.id, i["title"])'''
