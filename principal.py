#coding: utf-8
#https://www.youtube.com/watch?time_continue=598&v=fmf_y8zpOgA&feature=emb_logo
#https://imasters.com.br/back-end/como-fazer-web-scraping-com-python
import sys

import teste

def rodar(user):    
    import requests
    from urllib.request import urlopen

    headers = {}

    with requests.Session() as s:
        
        #carrega cookie
        #with open('cookie.txt','r') as arq:
        #    cookie = str(arq.readlines())
        teste.set_cookie()
        cookie = teste.get_cookie()
            
        #salva cookie no headers        
        headers['cookie'] = cookie    
        
        #receber nome do usuario
        #user = input("Nome do usuario: ")
        
        #faz req para site
        url = "https://cursos.alura.com.br/user/"+user+"/actions"
        r = s.get(url, headers=headers)
        
        #pega data e hora para colocar no topo do arquivo
        from datetime import datetime
        data_atual = datetime.now()
        
        #salva pagina em arquivo com data e hora do registro
        with open('teste.html','w') as arq:
            arq.writelines(str(data_atual))
            arq.writelines('\n')
            arq.writelines(str(r.content))

    import pegar_informacoes
    pegar_informacoes.rodar()
    #print("foi pergar info")
    import calculos

if __name__ == '__main__':
    for param in sys.argv :
        user = param
    rodar(user)
    import calculos
    calculos.rodar_calculos()