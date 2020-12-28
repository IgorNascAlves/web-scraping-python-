from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram.error import (TelegramError, BadRequest, 
                            TimedOut, NetworkError)

import datetime as dt    
import re
import os
from dotenv import load_dotenv

from principal import rodar
from calculos import descobre_quantidade_respostas, calculo_ano, descobre_quantidade_respostas_passada, roda_api
from atualiza_cookie import atualiza

roda_api()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def error_callback(update, context):
    try:
        raise context.error
    except TimedOut:
        dormi_aqui(update, context)
    except BadRequest:
        dormi_aqui(update, context)
    except NetworkError:
        dormi_aqui(update, context)
    except TelegramError:
        dormi_aqui(update, context)

def ano(update, context):    
    user = context.args[0]
    calcula_ano(update, context, user) 

def cookie(update, context):
    atualiza(str(context.args[0]))
    msg = "Atualizado"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def start(update, context):
    msg = "i am no longer a hunter, i am a nurse droid"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def echo(update, context):
    resposta = str(update.effective_user.full_name) + ", você esqueceu o comando /semana"
    context.bot.send_message(chat_id=update.effective_chat.id, text=resposta)

def semana(update, context):    
    user = context.args[0]
    calcula_semana(update, context, user) 

def semana_passada(update, context):    
    user = context.args[0]
    calcula_semana_passada(update, context, user) 

def igor(update, context):
    user = 'igor-nascimento-flipe'
    calcula_semana(update, context, user) 

def unknown(update, context):
    user = update.message.parse_entity(update.message.entities[0])[1:]
    calcula_semana(update, context, user)    

def calcula_ano(update, context, user):
    rodar(user)
    data = dt.datetime.now().date().strftime('%d/%m/%Y')
    padrao = '([0-9]{2})/([0-9]{2})/([0-9]{4})'
    resultado = re.search(padrao,data)
    data = dt.date(day=int(resultado.group(1)),
                month=int(resultado.group(2)),
                year=int(resultado.group(3)))
    _ = descobre_quantidade_respostas(data)
    calculo_ano()

    filename = 'total_por_mes.png'
    file_photo = open(filename, 'rb')

    context.bot.send_photo(chat_id=update.effective_chat.id, photo=file_photo)
    
    resposta = "DADOS NÃO CONFIÁVEIS, AINDA NÃO PASSOU NOS TESTES"
    context.bot.send_message(chat_id=update.effective_chat.id, text=resposta)
    
    file_photo.close()  

def calcula_semana(update, context, user):
    rodar(user)
    data = dt.datetime.now().date().strftime('%d/%m/%Y')
    padrao = '([0-9]{2})/([0-9]{2})/([0-9]{4})'
    resultado = re.search(padrao,data)
    data = dt.date(day=int(resultado.group(1)),
                month=int(resultado.group(2)),
                year=int(resultado.group(3)))
    _ = descobre_quantidade_respostas(data)

    filename = 'calculo_das_minhas_repostas.png'
    file_photo = open(filename, 'rb')

    context.bot.send_photo(chat_id=update.effective_chat.id, photo=file_photo)
    
    file_photo.close()

def calcula_semana_passada(update, context, user):
    rodar(user)
    data = dt.datetime.now().date().strftime('%d/%m/%Y')
    padrao = '([0-9]{2})/([0-9]{2})/([0-9]{4})'
    resultado = re.search(padrao,data)
    data = dt.date(day=int(resultado.group(1)),
                month=int(resultado.group(2)),
                year=int(resultado.group(3))) - dt.timedelta(days=7)
    _ = descobre_quantidade_respostas_passada(data, user)

    filename = 'calculo_das_minhas_repostas_passada.png'
    file_photo = open(filename, 'rb')

    context.bot.send_photo(chat_id=update.effective_chat.id, photo=file_photo)
    
    file_photo.close()
  
def dormi_aqui(update, context):
    resposta = "Desculpa " + str(update.effective_user.full_name) + ", dormi aqui, era isso que você queria ?"
    context.bot.send_message(chat_id=update.effective_chat.id, text=resposta)    
    comando = update.message.parse_entity(update.message.entities[0])[1:]    
    if(comando == 'semana'): 
        semana(update, context)
    elif (comando == 'ano'): 
        print("NOVO LOG:", context)
        ano(update, context)
    elif (comando == 'igor'): 
        igor(update, context)
    else: 
        unknown(update, context)

load_dotenv()
TOKEN = str(os.getenv('TOKEN_TELEGRAM'))
updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher

dispatcher.add_error_handler(error_callback)

cookie_handler = CommandHandler('cookie', cookie)
dispatcher.add_handler(cookie_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

ano_handler = CommandHandler('ano', ano)
dispatcher.add_handler(ano_handler)

semana_handler = CommandHandler('semana', semana)
dispatcher.add_handler(semana_handler)

passada_handler = CommandHandler('passada', semana_passada)
dispatcher.add_handler(passada_handler)

semana_handler = CommandHandler('igor', igor)
dispatcher.add_handler(semana_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()

updater.idle()
