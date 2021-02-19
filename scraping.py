import os
import re
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv


load_dotenv()

def executar_requisicao(user: str) -> bytes:    

    with requests.Session() as sessao:

        headers: dict = {'cookie': f"__cfduid=; caelum.login.token={os.getenv('COOKIE')}; alura.userId={os.getenv('USER_ID')};"}   
        url: str = f"https://cursos.alura.com.br/user/{user}/actions"
        resposta: requests.models.Response = sessao.get(url, headers=headers)

    return  resposta.content

def pegar_informacoes(pagina: bytes) -> None:

    data_hora_atual: datetime = datetime.now()

    #retira textos que começam com resposta e terminam com numeros
    regex: str = 'Resposta{1}.{0,100}rum.{0,100}.{0,100}.{0,100}[0-9]{1}'
    respostas: list = re.findall(regex,str(pagina))
    dados: str = ' '.join(respostas)

    #retira numero de dias ou horas ou semanas ou meses
    regex = '([0-9]*) (min|hor|dia|sem|m)'
    DHSM: list = re.findall(regex, dados)

    #retira datas no formato DD/MM/AAAA
    regex = '([0-9]{2}/[0-9]{2}/[0-9]{4})'
    data: list = re.findall(regex, dados)

    #criar lista de dados no formato DD/MM/AAAA
    data_registros: list = []    

    escalas_pt_en: dict = {'min': 'minutes',
                           'hor': 'hours',
                           'dia': 'days',
                           'sem': 'weeks',
                           'm': 'months'}

    for valor, escala in DHSM:
        formatar_horario(data_registros, data_hora_atual, escalas_pt_en[escala], valor)            
    
    for valor in data:
        data_registros.append(valor)

    if  not len(data_registros):
        raise IndexError("Registro de datas vazio, atualizar o cookie")

    with open('csv/datas_gerais_por_usuario.csv','w') as arq:
        for data in data_registros:
            arq.writelines(str(data)+"\n")

def formatar_horario(data_registros: list, data_hora_atual: datetime, escala: str, valor: str) -> None:
    data_registros.append((data_hora_atual - relativedelta(**{escala: int(valor)})).date().strftime("%d/%m/%Y"))

def pegar_dados(user: str) -> None:
    pagina = executar_requisicao(user)
    pegar_informacoes(pagina)

def atualiza_cookie(novo_cookie: str) -> None:    
    os.environ["COOKIE"] = novo_cookie
