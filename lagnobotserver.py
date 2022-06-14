from flask import Flask 
from threading import Thread # Run from a different thread from FabiBot

app = Flask('')

@app.route('/')
def home():
  return "Hello! I am alive!"

def run():
  app.run(host='0.0.0.0', port = 8080)

def keep_alive():
  t = Thread(target = run)
  t.start()

def keep_alive_magnus():
  c = Thread(target = run)
  c.start()


