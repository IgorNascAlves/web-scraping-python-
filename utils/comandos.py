import discord
import datetime as dt 
import pandas as pd

from utils.scraping import pegar_dados, atualiza_cookie
from utils.calculos import descobre_quantidade_respostas, roda_api, dados_api


async def semana_atual(message, usuario_alura):
    tempo = 'atual'
    try:
        pegar_dados(usuario_alura)
    except IndexError:
        print("Erro " + message.author.name) 
        await message.author.send(f'Vish {message.author.name} me perdi, chama o Igor :s')
    else:
        data = (dt.datetime.now() - dt.timedelta(hours=3)).date() # ajustando horario do servidor
        descobre_quantidade_respostas(data, tempo)
        await message.author.send(f'Olá {message.author.name}!', file=discord.File(f'img/respostas_semana_{tempo}.png')) 

async def semana_passada(message, usuario_alura): 
    dados_api(usuario_alura)
    tempo = 'passada'

    data = (dt.datetime.now() - dt.timedelta(days=7, hours=3)).date() # ajustando horario do servidor
    descobre_quantidade_respostas(data, tempo)

    await message.author.send(f'Olá {message.author.name}!', file=discord.File(f'img/respostas_semana_{tempo}.png'))

async def cookie(message, novo_cookie):
    atualiza_cookie(novo_cookie)
    await message.author.send('Atualizado')

async def lista_semana(message, nome_time):
    lista_users = pd.read_csv('csv/usuarios_por_time.csv').query("time == @nome_time")['user']
    
    tempo = 'atual'

    for usuario_alura in lista_users:
        try:
            pegar_dados(usuario_alura)
        except IndexError:
            print("Erro " + message.author.name) 
            await message.author.send(f'Vish {message.author.name} me perdi, chama o Igor :s')
        else:
            data = dt.datetime.now().date()        
            descobre_quantidade_respostas(data, tempo)
            await message.author.send(f'Semana atual de {usuario_alura}:', file=discord.File(f'img/respostas_semana_{tempo}.png'))

async def lista_passada(message, nome_time):
    lista_users = pd.read_csv('csv/usuarios_por_time.csv').query("time == @nome_time")['user']
    
    tempo = 'passada'
    data = dt.datetime.now().date() - dt.timedelta(days=7)

    for usuario_alura in lista_users:
        dados_api(usuario_alura)
        descobre_quantidade_respostas(data, tempo)
        await message.author.send(f'Semana passada de {usuario_alura}:', file=discord.File(f'img/respostas_semana_{tempo}.png'))