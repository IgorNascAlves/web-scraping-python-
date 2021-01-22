import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import re
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
load_dotenv()

#print(len(df))

def descobre_quantidade_respostas(today: dt.date):
    df = pd.read_csv('datas.csv', names = ['Date'], header=None, parse_dates=True, dayfirst=True, usecols=[0])
    eixo_x_grafico = []
    eixo_y_grafico = []

    dia = today.day

    dia_da_semana = today.isoweekday()
    
    if dia_da_semana == 7: dia_da_semana = 0

    #Dom Seg Ter Qua Qui Sex Sab
    #000 001 002 003 004 005 006
    #004 003 002 001 000 001 002
    
    dias = [today - dt.timedelta(i) for i in range(dia_da_semana,dia_da_semana-7,-1)]
    #dias.pop(0)
    #dias.pop(-1)
    #dias_antes = [today - dt.timedelta(i) for i in range(7-dia_da-semana,-1,-1)]
    
    #dias_depois = [today + dt.timedelta(i) for i in range(dia_da_semana,6,1)]
    
    #dias = dias_antes + dias_depois 
    
    quantidade = 0
    #i = 0
    for dia in dias: 
        #print(dia.strftime('%d/%m/%Y'))
        eixo_x_grafico.append(dia.strftime('%d/%m'))
    
    for dia in dias:
        quantidade += len(df[(df.Date == dia.strftime('%d/%m/%Y'))])
        respondeu_por_dia = len(df[(df.Date == dia.strftime('%d/%m/%Y'))])
        eixo_y_grafico.append(respondeu_por_dia)
    
    fig, ax = plt.subplots()
    legenda = ['Total na semana: ' + str(quantidade)]
    plt.title('Quantidade de respostas por dias da semana')
    plt.xlabel('Data')
    plt.ylabel('Quantidade')
    rects1 = plt.bar(eixo_x_grafico, eixo_y_grafico, width= 0.5)    
    plt.yticks(range(0,21,5))
    plt.legend(legenda)
    autolabel(rects1, ax)
    fig.tight_layout()
    plt.savefig('calculo_das_minhas_repostas.png')
    plt.clf()
    # plt.show()
    
    return quantidade

def rodar_calculos():
    data = input("Diga a data(dd/mm/yyyy) e eu te digo a quantidade de resposta desssa semana:")
    #dia = input("Informar o dia:") 
    #data = dia+'/03/2020' 
    #data = dt.datetime.now().date().strftime('%d/%m/%Y')

    padrao = '([0-9]{2})/([0-9]{2})/([0-9]{4})'
    resultado = re.search(padrao,data)
    data = dt.date(day=int(resultado.group(1)),
                month=int(resultado.group(2)),
                year=int(resultado.group(3)))

    print("Essa semana respondeu:",descobre_quantidade_respostas(data),sep=' ')

def calculo_ano():
    df = pd.read_csv("datas.csv", sep=',', header=None,
                    names=['Datas','sei la'], usecols=['Datas'],
                    parse_dates=[0], dayfirst=True)
    df = df[df.Datas.dt.strftime('%Y').str.contains("2020")]
    df_total_por_mes = df.groupby(df['Datas'].dt.strftime('%m/%y')).count()
    df_total_por_mes.columns=['Total']   
    
    fig, ax = plt.subplots()
    
    legenda = ['Total: ' + str(df_total_por_mes.sum()[0])]
    plt.title('Quantidade de respostas por mes')
    plt.xlabel('Data')
    plt.ylabel('Quantidade')
    rects1 = plt.bar(df_total_por_mes.index, df_total_por_mes.Total, width= 0.5)
    plt.legend(legenda)
    
    autolabel(rects1, ax)
    fig.tight_layout()

    plt.savefig('total_por_mes.png')
    plt.clf()      

def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

def descobre_quantidade_respostas_passada(today: dt.date, user: str):
    dados_api(user)
    df = pd.read_csv('passada.csv', names = ['Date'], header=None, parse_dates=True, dayfirst=True, usecols=[0])
    eixo_x_grafico = []
    eixo_y_grafico = []

    dia = today.day

    dia_da_semana = today.isoweekday()
    
    if dia_da_semana == 7: dia_da_semana = 0

    #Dom Seg Ter Qua Qui Sex Sab
    #000 001 002 003 004 005 006
    #004 003 002 001 000 001 002
    
    dias = [today - dt.timedelta(i) for i in range(dia_da_semana,dia_da_semana-7,-1)]
    #dias.pop(0)
    #dias.pop(-1)
    #dias_antes = [today - dt.timedelta(i) for i in range(7-dia_da-semana,-1,-1)]
    
    #dias_depois = [today + dt.timedelta(i) for i in range(dia_da_semana,6,1)]
    
    #dias = dias_antes + dias_depois 
    
    quantidade = 0
    #i = 0
    for dia in dias: 
        #print(dia.strftime('%d/%m/%Y'))
        eixo_x_grafico.append(dia.strftime('%d/%m'))
    
    for dia in dias:
        quantidade += len(df[(df.Date == dia.strftime('%Y-%m-%d'))])
        respondeu_por_dia = len(df[(df.Date == dia.strftime('%Y-%m-%d'))])
        eixo_y_grafico.append(respondeu_por_dia)
    
    fig, ax = plt.subplots()
    legenda = ['Total na semana: ' + str(quantidade)]
    plt.title('Quantidade de respostas por dias da semana')
    plt.xlabel('Data')
    plt.ylabel('Quantidade')
    rects1 = plt.bar(eixo_x_grafico, eixo_y_grafico, width= 0.5)    
    plt.yticks(range(0,21,5))
    plt.legend(legenda)
    autolabel(rects1, ax)
    fig.tight_layout()
    plt.savefig('calculo_das_minhas_repostas_passada.png')
    plt.clf()
    # plt.show()
    
    return quantidade

def dados_api(user: str):
    dados = pd.read_csv('dados.csv', parse_dates=[3], dayfirst=True).query('username == @user')[['creationDate']]
    dados['data'] = dados.creationDate.dt.date
    dados[['data']].to_csv('passada.csv', index=False, header=False, sep=',')

def roda_api():
    import pandas as pd
    ##with open("url.txt", "r") as f:
    ##    URL = f.read()
    URL = os.getenv('URL')
    dados = pd.read_csv(URL)
    dados.to_csv('dados.csv', index=False)