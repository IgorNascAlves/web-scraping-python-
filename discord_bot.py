import discord
import os
import datetime as dt 
from dotenv import load_dotenv
load_dotenv()

from principal import rodar
from calculos import descobre_quantidade_respostas, calculo_ano, descobre_quantidade_respostas_passada, roda_api

client = discord.Client()
@client.event
async def on_ready():
    print('Bot Online!')

@client.event
async def on_message(message):

    if message.content.startswith('/semana'):
        comando, usuario_alura = message.content.split()

        rodar(usuario_alura)
        data = dt.datetime.now().date()
        _ = descobre_quantidade_respostas(data)

        await message.author.send(f'Olá {message.author.name}!', file=discord.File('calculo_das_minhas_repostas.png'))

        # await message.channel.send(f'Hello {message.author}! - Bot em Python', file=discord.File('gráfico_teste.png')) # enviar no canal
TOKEN = os.getenv('TOKEN_DISCORD')
client.run(TOKEN)