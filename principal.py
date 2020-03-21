#https://www.youtube.com/watch?time_continue=598&v=fmf_y8zpOgA&feature=emb_logo
#https://imasters.com.br/back-end/como-fazer-web-scraping-com-python

import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

headers = {}

with requests.Session() as s:
    #carrega cookie
    with open('cookie.txt','r') as arq:
        cookie = str(arq.readlines())
    #salva cookie no headers        
    headers['cookie'] = cookie    
    #faz req para site
    url = "https://cursos.alura.com.br/user/igor-nascimento-flipe/actions"
    r = s.get(url, headers=headers)
    #salva pagina em arquivo
    with open('teste.html','w') as arq:
        arq.writelines(str(r.content))