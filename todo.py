# -*- coding: utf-8 -*-

'''

TO-DO

nombre:

1- /movie + id erronea: lanza error y crashea
2- /movie sin parametros mensaje

'''


'''@tb.inline_handler(lambda query: (query.query.startswith('cartelera') or query.query.startswith('now_palying') or query.query.startswith('encines'))
                   and len(query.query.split()) == 1)
def inline_cartelera(q):
    sendInlineQuery(tb, q.id, img_url, API_KEY_TMDB, "now_playing", 20)

@tb.inline_handler(lambda query: (query.query.startswith('upcoming') or query.query.startswith('featured') or query.query.startswith('porvenir') or query.query.startswith('proximamente'))
                   and len(query.query.split()) == 1)
def inline_upcoming(q):
    sendInlineQuery(tb, q.id, img_url, API_KEY_TMDB, "upcoming", 10)

@tb.inline_handler(lambda query: (query.query.startswith('top') or query.query.startswith('valoradas'))
                   and len(query.query.split()) == 1)
def inline_top(q):
    sendInlineQuery(tb, q.id, img_url, API_KEY_TMDB, "top_rated", 20)

@tb.inline_handler(lambda query: (query.query.startswith('populares') or query.query.startswith('popu') or query.query.startswith('pop'))
                   and len(query.query.split()) == 1)
def inline_popu(q):
    sendInlineQuery(tb, q.id, img_url, API_KEY_TMDB, "popular", 20)'''




'''def inline_search(q):
    try:
        #url = 'http://www.omdbapi.com/?s='+inline_query.query+'&apikey=31e230da'
        url = "https://api.themoviedb.org/3/search/movie?language=es-ES&api_key=" + API_KEY_TMDB + "&query=" + str(q.query).replace(" ", "+")
        print(url)
        response = requests.get(url)
        res = response.json()['total_results']
        data = response.json()['results']

        if(res!=0):
            show_list=[]
            
            for result in data[:10]:
                idfilm = result['id']
                picfilm = img_url + str(result['poster_path'])
                title = result['title']
                print(picfilm)

                if result['poster_path'] == "":
                    title = title.replace(" ", "+")
                    picfilm = 'https://placeholdit.imgix.net/~text?txtsize=90&bg=ffffff&txt=' + title + '&w=512&h=512&fm=jpg&txttrack=0.jpg'

                capfilm = 'Title: ' + title + '\n' + '\n' + 'IMDb:  ' + str(result["vote_average"]) + '/10   (' + str(result["vote_count"]) + ' votes)'
                #result = types.InlineQueryResultPhoto(idfilm, picfilm, picfilm, caption=capfilm)
                show_list.append(types.InlineQueryResultPhoto(idfilm, picfilm, picfilm, caption=capfilm))            

        else:
            show_list = [types.InlineQueryResultArticle('1', 'No movies found for: ' + q.query,
                                               types.InputTextMessageContent('Content not found in IMDb!'))]
            
        tb.answer_inline_query(q.id, show_list, cache_time=1)
    except Exception as e:
        print("Exception: ",str(e))'''