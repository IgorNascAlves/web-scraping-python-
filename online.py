from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Olá, sou IG-11"

def run():
  app.run(host='0.0.0.0')

def keep_alive():
    t = Thread(target=run)
    t.start()