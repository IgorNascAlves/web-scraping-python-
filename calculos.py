import pandas as pd
import datetime as dt
import re

df = pd.read_csv('teste.csv', names = ['Date'], header=None, parse_dates=True, dayfirst=True, usecols=[0])

#print(len(df))

def descobre_quantidade_respostas(today: dt.date):
    
    dia = today.day

    dia_da_semana = today.isoweekday()
    
    if dia_da_semana == 7: dia_da_semana = 0

    #Dom Seg Ter Qua Qui Sex Sab
    #000 001 002 003 004 005 006
    #004 003 002 001 000 001 002
    
    dias = [today - dt.timedelta(i) for i in range(dia_da_semana,dia_da_semana-7,-1)]
    
    #dias_antes = [today - dt.timedelta(i) for i in range(7-dia_da-semana,-1,-1)]
    
    #dias_depois = [today + dt.timedelta(i) for i in range(dia_da_semana,6,1)]
    
    #dias = dias_antes + dias_depois 
    
    quantidade = 0
    i = 0
    for dia in dias: print(dia.strftime('%d/%m/%Y'))
    
    for dia in dias:
        quantidade += len(df[(df.Date == dia.strftime('%d/%m/%Y'))])
    
    return quantidade

#data = input("Diga a data(dd/mm/yyyy) e eu te digo a quantidade de resposta desssa semana:")
#dia = input("Informar o dia:") 
#data = dia+'/03/2020' 
data = dt.datetime.now().date().strftime('%d/%m/%Y')

padrao = '([0-9]{2})/([0-9]{2})/([0-9]{4})'
resultado = re.search(padrao,data)
data = dt.date(day=int(resultado.group(1)),
               month=int(resultado.group(2)),
               year=int(resultado.group(3)))

print("Essa semana respondeu:",descobre_quantidade_respostas(data),sep=' ')