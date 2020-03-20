with open('saida.html','r') as arq:
    pagina = str(arq.readlines())
#print(pagina)
import re

#Resposta a t\xc3\xb3pico do f\xc3\xb3rum\n                            </td>\n                            <td #class="actions-table-actionDate">\n                                    7 horas atr\xc3\xa1s\n                            
# </td>\n  

#regex = 'Resposta{1}.{0,27}.{0,5}[0-5]rum{1}'
regex = 'Resposta{1}.{0,100}rum.{0,100}.{0,100}.{0,100}[0-9]{1}'
#print(re.search(regex,str(pagina)).group())
print(len(re.findall(regex,str(pagina))))
print(re.findall(regex,str(pagina))[70])
#print(len(re.findall(regex,str(pagina))[0])-len('Resposta'))