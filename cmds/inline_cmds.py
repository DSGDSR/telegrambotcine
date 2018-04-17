from bot import telebot, tb, os, implist, API_KEY_TMDB, requests, img_url, conn, c, math
from extra.funcs import *
from telebot import *

################################################
#################### INLINE ####################
################################################

implist.append(os.path.basename(__file__))

@tb.inline_handler(lambda query: query.query.lower() == 'help' or query.query == '' )
def inline_help(q):
    inline = types.InlineQueryResultArticle(1,
                                            "AYUDA",
                                            types.InputTextMessageContent("/help", parse_mode="Markdown"),
                                            description="Muestra ayuda sobre las consultas posibles al bot",
                                            thumb_url='http://dev.dsgdsr.me/botcine/help.jpg')
    tb.answer_inline_query(q.id, [inline], cache_time=1)

@tb.inline_handler(lambda query: True)
def inline_search(q):
    try:
        lista_query = []
        url = "https://api.themoviedb.org/3/search/movie?language=es-ES&api_key=" + str(API_KEY_TMDB) + "&query=" + str(q.query)
        response = requests.get(url)
        idp=1
        res = response.json()['total_results']
        data = response.json()['results']

        if(res!=0):
            for i in data:
                if(i['backdrop_path'] is None):
                    pic = 'https://placeholdit.imgix.net/~text?txtsize=90&bg=ffffff&txt=' + str(i['title']).replace(" ", "+") + '&w=512&h=512&fm=jpg&txttrack=0.jpg'
                else:
                    pic = img_url + str(i['backdrop_path'])
                stro = "[⁣]("+ str(pic) + ")" + '*' + str(i['title']) + '*' + '\n\n*Fecha de salida*: ' + str(i['release_date']) + '\n*Puntuación*: ' + str(i['vote_average']) + ' (' + str(i['vote_count']) + ' votes)' + '\n\n*Sinopsis*: ' + str(ellipsis_str(i['overview'], i['id']))
                kb = types.InlineKeyboardMarkup()
                st = getState(q.from_user.id, i['id'], conn, c)
                if(st==None):
                    kb.add(types.InlineKeyboardButton('🕑  Pendiente', callback_data='add_pend ' + str(i['id'])),
                        types.InlineKeyboardButton('✅  Vista', callback_data='add_seen ' + str(i['id'])))
                elif(st==1):
                    kb.add(types.InlineKeyboardButton('❌  Eliminar de lista', callback_data='del_movie ' + str(i['id'])))
                elif(st==0):
                    kb.add(types.InlineKeyboardButton('✅  Ya la he visto!', callback_data='set_seen ' + str(i['id'])))
                    kb.add(types.InlineKeyboardButton('❌  Eliminar de pendientes', callback_data='del_movie ' + str(i['id'])))
                lista_query.append(types.InlineQueryResultArticle(i['id'],
                                                        i['title'],
                                                        types.InputTextMessageContent(stro, parse_mode="Markdown"),
                                                        description=i['overview'],
                                                        thumb_url=pic,
                                                        reply_markup=kb,
                                                        hide_url=True))
                #lista_query.append(types.InlineQueryResultPhoto(i['id'], photo_url=pic, caption="HI", thumb_url=pic, reply_markup=kb))
                idp+=1

        else:
            lista_query = [types.InlineQueryResultArticle(9999999, 'No movies found for: ' + q.query,
                                               types.InputTextMessageContent('No movies found for: ' + q.query))]

        tb.answer_inline_query(q.id, lista_query, cache_time=1)
    except:
        pass

