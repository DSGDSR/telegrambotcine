import telebot
from telebot import *
import requests

def sendInlineQuery(tb, idu, img, api, query, l):
    try:
        lista_query = []
        url = "https://api.themoviedb.org/3/movie/" + str(query) + "?language=es-ES&api_key=" + str(api)
        response = requests.get(url)
        data = response.json()['results']
        idp=1
        for i in data[:int(l)]:
            lista_query.append(types.InlineQueryResultArticle(idp, 
                                                       i['title'], 
                                                       types.InputTextMessageContent("[⁣]("+ img+i['backdrop_path'] + ")"+"\n"+'*'+i['title']+'*'+'\n\n'+i['overview'], parse_mode="Markdown"),
                                                                                     description=i['overview'],
                                                                                     thumb_url=img+i['backdrop_path'],
                                                                                     hide_url=True))
            idp+=1

        tb.answer_inline_query(idu, lista_query, cache_time=1)
    except:
        pass


def sendInlineSearch(tb, idu, img, api, query, l):
    try:
        lista_query = []
        url = "https://api.themoviedb.org/3/search/movie?language=es-ES&api_key=" + str(api) + "&query=" + str(query)
        response = requests.get(url)
        data = response.json()['results']
        idp=1
        for i in data[:int(l)]:
            lista_query.append(types.InlineQueryResultArticle(idp, 
                                                       i['title'], 
                                                       types.InputTextMessageContent("[⁣]("+ img +i['backdrop_path'] + ")"+"\n"+'*'+i['title']+'*'+'\n\n'+i['overview'], parse_mode="Markdown"),
                                                       description=i['overview'],
                                                       thumb_url=img+i['backdrop_path'],
                                                       hide_url=True))
            idp+=1

        tb.answer_inline_query(idu, lista_query, cache_time=1)
    except:
        pass


def searchFilm(tb, api, query):
    try:
        url = "https://api.themoviedb.org/3/search/movie?language=es-ES&api_key=" + str(api) + "&query=" + str(query)
        response = requests.get(url)
        data = response.json()['results']
        head = "Has buscado: *" + query + "*\n\n"
        lista = ""
        idp=1
        for f in data[:7]:
            fstr = str(idp) + ".- " + f['title'] + "\n"
            lista += fstr
            idp+=1
        foo = "\nHaz click en cualquier película para ver la información"
        t = head + lista + foo

        return t
    except:
        pass


def searchSec(tb, api, query):
    try:
        url = "https://api.themoviedb.org/3/movie/" + str(query) + "?language=es-ES&api_key=" + str(api)
        response = requests.get(url)
        data = response.json()['results']
        head = "*Esta es la cartelera actual:*\n\n"
        lista = ""
        idp=1
        imgurl = "https://image.tmdb.org/t/p/w500" + data[0]['backdrop_path']
        for f in data[:7]:
            fstr = str(idp) + ".- " + f['title'] + "\n"
            lista += fstr
            idp+=1
        foo = "\nHaz click en cualquier película para ver la información"
        t = head + lista + foo
        msg = [t,imgurl]

        return msg
    except:
        pass


def getFilmInfo():
    pass