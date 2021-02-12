import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import re
import os
from dotenv import load_dotenv
load_dotenv()


def descobre_quantidade_respostas(hoje: dt.date, tempo: str) -> int:    

    fonte_dados = {'semana_atual': 'datas.csv', 'semana_passada': 'datas_gerais.csv'}

    datas = pd.read_csv(fonte_dados[tempo], names = ['Data'], header=None, parse_dates=['Data'], dayfirst=True, usecols=[0])
    
    dia_da_semana = hoje.isoweekday()
    
    if dia_da_semana == 7: dia_da_semana = 0
    
    dias = [hoje - dt.timedelta(num_dia) for num_dia in range(dia_da_semana,dia_da_semana-7,-1)]
    
    total_respostas_semana = len(datas.query('Data in @dias'))
    desenha_grafico(dias, datas, total_respostas_semana,'Quantidade de respostas por dias da semana')
    
    return total_respostas_semana

def desenha_grafico(dias: list, datas: pd.DataFrame, total_respostas_semana: int, nome_grafico: str) -> None:
    
    eixo_x_grafico = []
    eixo_y_grafico = []

    for dia in dias:
        dia_str = dia.strftime('%d/%m')
        eixo_x_grafico.append(dia_str)
        respondeu_por_dia = len(datas.query('Data == @dia'))
        eixo_y_grafico.append(respondeu_por_dia)
    
    ax = plt.subplot()
    plt.bar(eixo_x_grafico, eixo_y_grafico, width= 0.5, color='#167bf7')
    plt.title(nome_grafico)    
    plt.yticks(range(0,21,5))
    plt.legend([f'Total na semana: {total_respostas_semana}'])

    for i, valor in enumerate(eixo_y_grafico):
        if valor > 0:
            color = 'green' if valor > 5 else 'red'
            ax.text(x=i, y=valor+.5, s=str(valor), ha='center', color=color)
        
    plt.savefig('calculo_das_minhas_repostas.png')
    plt.clf()

def dados_api(usuario: str) -> None:
    dados = pd.read_csv('dados.csv', parse_dates=[3], dayfirst=True).query('username == @usuario')[['creationDate']]
    dados['data'] = dados.creationDate.dt.date
    dados[['data']].to_csv('datas_gerais.csv', index=False, header=False)

def roda_api() -> None:
    URL = os.getenv('URL')
    dados = pd.read_csv(URL)
    dados.to_csv('dados.csv', index=False)