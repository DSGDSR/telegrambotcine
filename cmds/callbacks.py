from bot import telebot, tb, os, implist, API_KEY_TMDB, requests, img_url, conn, c, math
from extra.funcs import *
from telebot import *

###################################################
#################### CALLBACKS ####################
###################################################

implist.append(os.path.basename(__file__))

@tb.callback_query_handler(func=lambda call: call.data.startswith('add_pend'))
def add_pend_handler(call):
    idu = call.from_user.id
    idp = extract_arg(call.data)
    addM = addMovie(idu, idp[0], pend, conn, c)
    tb.edit_message_text(text="asd",
                          chat_id=call.message.chat.id,
                            message_id=call.message.message_id)
    if(addM == None):
        tb.send_message(call.from_user.id, "La película ya esta en tu lista de pendientes", parse_mode="Markdown")
    else:
        tb.send_message(call.from_user.id, "Película añadida a pendientes", parse_mode="Markdown")

@tb.callback_query_handler(func=lambda call: call.data.startswith('add_seen'))
def add_seen_handler(call):
    idu = call.from_user.id
    idp = extract_arg(call.data)
    addM = addMovie(idu, idp[0], seen, conn, c)
    if(addM == None):
        tb.send_message(call.from_user.id, "La película ya esta en tu lista de vistas", parse_mode="Markdown")
    else:
        tb.send_message(call.from_user.id, "Película añadida a vistas", parse_mode="Markdown")

@tb.callback_query_handler(func=lambda call: call.data.startswith('set_seen'))
def set_seen_handler(call):
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
def del_movie_handler(call):
    idu = call.from_user.id
    idp = extract_arg(call.data)
    delM = delMovie(idu, idp[0], conn, c)
    if(delM == None):
        tb.send_message(call.from_user.id, "Error: La película no se encuentra en tu lista", parse_mode="Markdown")
    else:
        tb.send_message(call.from_user.id, "Película eliminada de la lista!", parse_mode="Markdown")
