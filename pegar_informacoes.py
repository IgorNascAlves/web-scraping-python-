#coding: utf-8
#le arquivo
with open('teste.html','r') as arq:
    pagina = str(arq.readlines())

#pegar data e hora do arquivo
import re
regex = '([0-9]{4})-([0-9]{1,2})-([0-9]{1,2}) ([0-9]{2})'
data_hora_atual = re.search(regex,str(pagina))
from datetime import datetime, timedelta
if data_hora_atual:
    data_hora_atual = datetime(year=int(data_hora_atual.group(1)),month=int(data_hora_atual.group(2)),
                   day=int(data_hora_atual.group(3)),hour=int(data_hora_atual.group(4)))

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
from dateutil.relativedelta import relativedelta
data_registros = []
for valor in DHSM:
    if valor[1] == 'minutos' or valor[1] == 'minuto':
        data_registros.append((data_hora_atual - timedelta(minutes=int(valor[0]))).date().strftime("%d/%m/%Y"))
    elif valor[1] == 'horas' or valor[1] == 'hora':
        data_registros.append((data_hora_atual - timedelta(hours=int(valor[0]))).date().strftime("%d/%m/%Y"))
    elif valor[1] == 'dias' or valor[1] == 'dia':
        data_registros.append((data_hora_atual - timedelta(days=int(valor[0]))).date().strftime("%d/%m/%Y"))
    elif valor[1] == 'semanas' or valor[1] == 'semana':
        data_registros.append((data_hora_atual - timedelta(weeks=int(valor[0]))).date().strftime("%d/%m/%Y"))
    elif valor[1] == 'm':
        data_registros.append((data_hora_atual - relativedelta(months = int(valor[0]))).date().strftime("%d/%m/%Y"))
    else:
        print(valor)
for valor in data:
    data_registros.append(valor)
    
#salvar em arquivo csv
with open('teste.csv','w') as arq:
    for data in data_registros:
        arq.writelines(str(data)+",\n")
