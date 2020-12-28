
def atualiza(novo_cookie):    
    inicio = "__cfduid=; caelum.login.token="
    fim = "; alura.userId=109951;"
    novo = inicio + novo_cookie + fim

    with open('cookie.txt','w') as arq:
        arq.writelines(novo)   