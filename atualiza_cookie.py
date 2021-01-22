import os

def atualiza(novo_cookie):    
    #with open('.env','r+') as arq:
    #    arq.seek(239)
    #    arq.write('\nCOOKIE=' + novo_cookie)
    os.environ["COOKIE"] = novo_cookie