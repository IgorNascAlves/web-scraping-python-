import base64

def set_cookie():
    with open('cookie.txt','r') as arq:
        cookie = str(arq.readlines())
        cod_cookie = base64.b64encode(cookie.encode("utf-8"))
        #print(cod_cookie)

    with open('cod.txt','w') as arq:
        arq.writelines(str(cod_cookie))   

    
def get_cookie():
    with open('cod.txt','r') as arq:
        cod_cookie = arq.readline()[2:-1]
        #print(cod_cookie)
        cookie = base64.b64decode(cod_cookie).decode("utf-8")  
    return cookie