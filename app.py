import json
import requests
import os
import dotenv

from flask import Flask
from flask import request
from flask import Response
from flask_sqlalchemy import SQLAlchemy

# Get env variables TODO should be separated
dotenv.load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
NGROK_URL = os.getenv('NGROK_URL')      

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./esperanzo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
  id = db.Column('id', db.Integer, primary_key = True)
  first_name = db.Column('first_name', db.String(100))
  last_name = db.Column('last_name', db.String(100))

  def __init__(self, id, first_name, last_name):
    self._id = id
    self.first_name = first_name
    self.last_name = last_name 

  def __repr__(self):
    '''
      What will be displayed if a User is called from the print() method
    '''
    return f'id: {self.id}, first_name: {self.first_name}, last_name: {self.last_name}'

def write_json(data, filename='response.json'):
  '''
    This function will write a json object into the directory

    Args:
      data (json): json object
  '''
  with open(filename, 'w') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

def send_message(chat_id, msg):
  '''
    Will send a message to the current given chat-id

    Args:
      chat_id (str): chat id in string format
      msg (str): message to send
    
    Returns:
      (tbd)
  '''
  url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
  # define a json object to send via requests
  json = {
    'chat_id': chat_id,
    'text': msg
  }
  r = requests.post(url, json=json)
  return r

@app.route('/webhook', methods=['GET'])
def webhook():
  '''
    Workaround to set the webhook -> should be another thing
  '''
  print('Setting the webhook for telegram')
  url = f'https://api.telegram.org/bot{BOT_TOKEN}/setWebHook?url={NGROK_URL}'
  print(url)
  res = requests.get(url)
  json_res = res.json()
  
  print(json_res['description'])

  return json_res

@app.route("/", methods = ['POST', 'GET'])
def index():
  if request.method == 'POST':
    msg = request.get_json() # the msg obj will be a json sent by telegram

    write_json(msg, 'telegram_request.json')

    chat_id = msg['message']['chat']['id'] # get the chat id to respond
    # if greet command then respond with hi :D!
    if msg['message']['text'] == '/greet':
      send_message(chat_id, 'Hola patrona :D!')

      return Response('ok', status = 200) # have to return 200 so telegram doesnt explode?

    # we have to return the 200 response code so that telegram gets that we have received its msg
    return Response('ok', status=200)
  else:
    return '<h1> Esperanzo todo Bot </h1>'

if __name__ == '__main__':
  db.create_all() #initialize the db if it doesn't already exists

  # if we run the script via the command line it will enter debug mode automatically
  app.run(debug=True)
  
