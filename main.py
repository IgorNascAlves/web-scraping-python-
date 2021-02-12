import discord
import os
import datetime as dt 
from dotenv import load_dotenv
load_dotenv()

from online import keep_alive

from scraping import pegar_dados, atualiza_cookie
from calculos import descobre_quantidade_respostas, roda_api, dados_api

client = discord.Client()
@client.event
async def on_ready():
    print('Bot Online!')

@client.event
async def on_guild_join(guild):
    general = discord.utils.find(lambda x: x.name == 'geral',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Olá Scuba Team, eu sou o IG-11 e estou aqui para **quantificar seus tópicos no fórum diariamente**. Me chame no privado com o seguinte comando:\n ```/semana seunomedeusuariodaalura```\nEspero por vocês!')

@client.event
async def on_message(message):

    if message.content.startswith('/semana'):
        _, usuario_alura = message.content.split()

        try:
          pegar_dados(usuario_alura)
        except IndexError:
          print("Erro " + message.author.name) 
          await message.author.send(f'Vish {message.author.name} me perdi, chama o Igor :s')
        else:
          #data = (dt.datetime.now() - dt.timedelta(hours=3)).date()
          data = dt.datetime.now().date()        
          _ = descobre_quantidade_respostas(data, 'semana_atual')
          await message.author.send(f'Olá {message.author.name}!', file=discord.File('calculo_das_minhas_repostas.png'))

        print(message.author.name)        

        # await message.channel.send(f'Hello {message.author}! - Bot em Python', file=discord.File('gráfico_teste.png')) # enviar no canal

    if message.content.startswith('/passada'):
        roda_api()
        
        _, usuario_alura = message.content.split()

        dados_api(usuario_alura)

        #data = (dt.datetime.now() - dt.timedelta(days=7, hours=3)).date()
        data = dt.datetime.now().date() - dt.timedelta(days=7)
        _ = descobre_quantidade_respostas(data, 'semana_passada')

        print(message.author.name)

        await message.author.send(f'Olá {message.author.name}!', file=discord.File('calculo_das_minhas_repostas.png'))

    if message.content.startswith('/cookie'):
      _, novo_cookie = message.content.split()

      atualiza_cookie(novo_cookie)

      print(message.author.name)

      await message.author.send('Atualizado')
    
    if message.content.startswith('/lista_semana'):
        lista_users = message.content.split()[1:]

        for usuario_alura in lista_users:
          try:
            pegar_dados(usuario_alura)
          except IndexError:
            print("Erro " + message.author.name) 
            await message.author.send(f'Vish {message.author.name} me perdi, chama o Igor :s')
          else:
            data = dt.datetime.now().date()        
            _ = descobre_quantidade_respostas(data, 'semana_atual')
            await message.author.send(f'Semana atual de {usuario_alura}:', file=discord.File('calculo_das_minhas_repostas.png'))

        print(message.author.name)     

    if message.content.startswith('/lista_passada'):
        roda_api()
        lista_users = message.content.split()[1:]

        data = dt.datetime.now().date() - dt.timedelta(days=7)

        for usuario_alura in lista_users:
          dados_api(usuario_alura)
          _ = descobre_quantidade_respostas(data, 'semana_passada')
          await message.author.send(f'Semana passada de {usuario_alura}:', file=discord.File('calculo_das_minhas_repostas.png'))

TOKEN = os.getenv('TOKEN_DISCORD')
keep_alive()
client.run(TOKEN)