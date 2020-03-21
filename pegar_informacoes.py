#le arquivo
with open('teste.html','r') as arq:
    pagina = str(arq.readlines())
    
import re

#Resposta a t\xc3\xb3pico do f\xc3\xb3rum\n                            </td>\n                            <td #class="actions-table-actionDate">\n                                    7 horas atr\xc3\xa1s\n                            
# </td>\n  

#retira textos que começam com resposta e terminam com numeros
regex = 'Resposta{1}.{0,100}rum.{0,100}.{0,100}.{0,100}[0-9]{1}'
respostas = re.findall(regex,str(pagina))
print(len(respostas))
dados = ' '.join(respostas)
#retira numero de dias ou horas ou semanas ou meses
regex = '([0-9]*) (dias?|horas?|semanas?|m)'
DHSM = re.findall(regex, dados)
#retira datas no formato DD/MM/AAAA
regex = '([0-9]{2}/[0-9]{2}/[0-9]{4})'
data = re.findall(regex, dados)
#imprime soma dos resultados para comparar com o numero de respostas e tambem imprime os valores
print(len(data)+len(DHSM))
print(DHSM+data)