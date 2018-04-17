# -*- coding: UTF-8 -*-
# encoding=utf8

from extra.funcs import *
import math
import json
from extra import importdir
from extra.pycolors import *
import telebot
from telebot import *
import requests
from db.db import *
import time, sys, os, traceback

img_url = "https://image.tmdb.org/t/p/w500"
conn = sqlite3.connect('db/users.db', check_same_thread = False)
c = conn.cursor()
#c.execute("DROP TABLE movie_user")
#c.execute("""CREATE TABLE IF NOT EXISTS movie_user (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, movie TEXT, estado INTEGER)""")

with open('extra/config.json', 'r') as f:
    cfg = json.load(f)

TOKEN = cfg['token']
API_KEY_TMDB = cfg['omdb_api']
ver = cfg['version']

tb = telebot.TeleBot(TOKEN)

time.sleep(1)

##################################################
#################### COMANDOS ####################
##################################################

implist=[]
try:
    importdir.do('cmds', locals())
    print(pycol.OKGREEN + pycol.BOLD + str(len(implist)) + " commands imported with no erros: " + pycol.ENDC +
          pycol.OKGREEN +  ", ".join(implist) + pycol.ENDC)
except Exception as e:
    print(pycol.WARNING + pycol.BOLD + "\nUnexpected error while importing commands!: " + pycol.ENDC + str(e))
    print(traceback.format_exc() + '\n')


tb.polling(none_stop=True, interval=0, timeout=3)
