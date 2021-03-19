def registra_historico(message, parametro, comando):
    with open('csv/historico_uso.csv','a', encoding='UTF-8') as arq:
       arq.write(f"{message.author.name},{dt.datetime.now()},{parametro},{comando}\n")