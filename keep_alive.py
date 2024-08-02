from threading import Thread
from flask import Flask
import os
import time

PORT = os.environ.get('PORT')
start_time = time.time()
bot = Flask(__name__)

@bot.route('/')
def home():
  end_time = time.time()
  uptime_seconds = end_time - start_time
  uptime_minutes = uptime_seconds / 60
  response = f"Bot uptime: {uptime_minutes:.2f} minutes"
  response += f"\n\nLeeching Jobs from sources listed below:\n{os.environ.get('JOBS')}"
  response += f"\n\nLeeching Credit Cards from sources listed below:\n{os.environ.get('CC')}"
  return response

def run():
  bot.run(host = '0.0.0.0', port = PORT)

def keep_alive():
  t = Thread(target=run)
  t.start()
