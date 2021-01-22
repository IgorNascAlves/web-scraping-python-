import sys
import os
import re
import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from urllib.request import urlopen


load_dotenv()

def executar_requisicao(user: str) -> bytes:    

    with requests.Session() as sessao:

        headers = {'cookie': f"__cfduid=; caelum.login.token={os.getenv('COOKIE')}; alura.userId={os.getenv('USER_ID')};"}   
        url = f"https://cursos.alura.com.br/user/{user}/actions"
        resposta = sessao.get(url, headers=headers)

    return  resposta.content


def pegar_informacoes(pagina: bytes) -> None:

    data_hora_atual = datetime.now()

    #retira textos que começam com resposta e terminam com numeros
    regex = 'Resposta{1}.{0,100}rum.{0,100}.{0,100}.{0,100}[0-9]{1}'
    respostas = re.findall(regex,str(pagina))
    dados = ' '.join(respostas)

    #retira numero de dias ou horas ou semanas ou meses
    regex = '([0-9]*) (minutos?|horas?|dias?|semanas?|m)'
    DHSM = re.findall(regex, dados)

    #retira datas no formato DD/MM/AAAA
    regex = '([0-9]{2}/[0-9]{2}/[0-9]{4})'
    data = re.findall(regex, dados)

    #criar lista de dados no formato DD/MM/AAAA
    data_registros = []
    for valor in DHSM:
        print(data_registros)
        if valor[1] == 'minutos' or valor[1] == 'minuto':
            formatar_horario(data_registros, data_hora_atual, "minutes", valor[0])
        elif valor[1] == 'horas' or valor[1] == 'hora':
            formatar_horario(data_registros, data_hora_atual, "hours", valor[0])
        elif valor[1] == 'dias' or valor[1] == 'dia':
            formatar_horario(data_registros, data_hora_atual, "days", valor[0])
        elif valor[1] == 'semanas' or valor[1] == 'semana':
            formatar_horario(data_registros, data_hora_atual, "weeks", valor[0])
        elif valor[1] == 'm':
             formatar_horario(data_registros, data_hora_atual, "months", valor[0])
    
    for valor in data:
        data_registros.append(valor)

    if  not len(data_registros):
        raise Exception("Atualizar o cookie")

    with open('datas.csv','w') as arq:
        for data in data_registros:
            arq.writelines(str(data)+",\n")

def formatar_horario(data_registros, data_hora_atual, escala, valor):
    data_registros.append((data_hora_atual - relativedelta(**{escala: int(valor)})).date().strftime("%d/%m/%Y"))

def pegar_dados(user):
    pagina = executar_requisicao(user)
    pegar_informacoes(pagina)
