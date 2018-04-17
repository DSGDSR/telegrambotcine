from bot import telebot, tb, os, implist

implist.append(os.path.basename(__file__))

@tb.message_handler(commands=['help'])
def helpc(m):
    presentacion = "*Ayuda* \nLos comandos In-Line no deben enviarse, sólo colocarlos en la línea de texto. \n"
    comandos = "Aquí se exponen todos los comandos: \n=> upcoming - devuelve un listado con las películas a estrenar \n=> valoradas - devuelve un listado con las películas más valoradas \n=> populares - devuelve un listado con las películas populares del momento.\n=> cartelera - devuelve un listado con las películas actualmente en los cines.\nSi sólo se escribe el nombre de la película, se hará una búsqueda de ella.\n\n"
    spam = "Bot creado por @Skr0tex, @andresitoperson y @davidsnchz99"
    txt = presentacion + comandos + spam
    tb.send_message(m.chat.id, txt, parse_mode="Markdown")