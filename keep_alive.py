from threading import Thread
from flask import Flask
from config import Port
import os
import time

PORT = os.environ.get('PORT')
start_time = time.time()
bot = Flast(__name__)

@bot.route('/')
def home():
  end_time = time.time()
  uptime_secconds = end_time - start_time
  uptime_minutes = uptime_seconds / 60
  return f'Bot uptime: {uptime_minutes:.2f} minutes'

def run():
  bot.run(host = '0.0.0.0', port = PORT)

def keep_alive():
  t = Thread(target=run)
  t.start()
