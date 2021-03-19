import discord
import os
import datetime as dt 
from dotenv import load_dotenv

from online import keep_alive
from utils.comandos import semana_atual, semana_passada, cookie, lista_semana, lista_passada, ranking_acessos
from utils.util import registra_historico

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print('Bot Online!')

@client.event
async def on_guild_join(guild):
    """
    Essa função é executada quando o bot é adcionado a um servidor, ela procura pelo canal geral e faz a apresentação do bot.
    """
    general = discord.utils.find(lambda canal: canal.name == 'geral',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Olá Scuba Team, eu sou o IG-11 e estou aqui para **quantificar seus tópicos no fórum diariamente**. Me chame no privado com o seguinte comando:\n ```/semana seunomedeusuariodaalura```\nEspero por vocês!')

@client.event
async def on_message(message):
    """
    Essa função é executada quando recebe uma mensagem.
    """
    
    if message.content.startswith('/'):
        comando, valor = message.content.split() # comando
        registra_historico(message, valor, comando)

        dicionario = {'/semana': semana_atual,
                    '/passada': semana_passada,
                    '/cookie': cookie,
                    '/lista_semana': lista_semana,
                    '/lista_passada': lista_passada,
                    '/top': ranking_acessos
                    }
        
        await dicionario[comando](message, valor)

TOKEN = os.getenv('TOKEN_DISCORD')
keep_alive()
client.run(TOKEN)
