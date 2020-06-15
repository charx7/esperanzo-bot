import json
import requests
import os

from esperanzo_bot import app # custom package import
from esperanzo_bot import db
from esperanzo_bot.models import Users, Todos

from flask import Flask
from flask import request
from flask import Response
from flask_sqlalchemy import SQLAlchemy

# get the BOT_TOKEN env variable -> this should be passed from run.py
BOT_TOKEN = os.getenv('BOT_TOKEN')

def write_json(data, filename='response.json'):
  '''
    This function will write a json object into the directory

    Args:
      data (json): json object
  '''
  with open('./esperanzo_bot/' + filename, 'w') as f:
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
    msg_from = msg['message']['from']['id'] # get the id of the person that sent the msg

    #########################################################################
    ##### Switch statements TODO: this should be processed via NLP and intent
    #########################################################################
    msg_text = msg['message']['text'] 
    #### /greet command logic
    if msg_text == '/greet':
      send_message(chat_id, 'Hey Patrona! 👋')

      return Response('ok', status = 200) # have to return 200 so telegram doesnt explode?
    
    #### /register command
    elif msg_text == '/register':
      # check if the user already exists on the 'Users' table
      found_user = Users.query.filter_by(id = msg_from).first()

      if found_user:
        send_message(chat_id, 'You are already registered :P /add to add a `TODO`.')
        return Response('ok', status = 200)

      else:
        f_n = msg['message']['from']['first_name']
        u_n = msg['message']['from']['username']
        new_usr = Users(id = msg_from, first_name = f_n, last_name= u_n)
        db.session.add(new_usr)
        db.session.commit() # TODO there is no way of knowing if the insert was succesful :/?

        send_message(chat_id, 'NICE! Now you can add a `TODO` by using the `/add <TEXT>` command 👨‍💻')
        
        return Response('ok', status=200)
    
    #### /add command
    elif msg_text[:4] == '/add':
      found_user = Users.query.filter_by(id = msg_from).first()
      if found_user:
        todo_text = msg_text[4:].strip()
        todo_to_add = Todos(todo_text=todo_text, owner_id=msg_from)
        db.session.add(todo_to_add)
        db.session.commit()
        send_message(chat_id, 'Added your new task.')
        
        return Response('ok', status = 200)

      else:
        send_message(chat_id, 'You need to register yourself via the /register command first :(')
        return Response('ok', status = 200)
    
    #### /remind command
    elif msg_text == '/remind':
      # case1 they are not registered
      # case2 they dont have any todos
      # case3 return a list of all the todos

      found_user = Users.query.filter_by(id = msg_from).first()
      if found_user:
        # query all the todos of the user
        if len(found_user.todos) > 0:
          bot_response = 'Your pending tasks are: '
          for todo in found_user.todos:
            curr_text = todo.todo_text
            bot_response = bot_response + '\n -' + curr_text
          send_message(chat_id, bot_response) # respond with the builded list
        else:
          send_message(chat_id, 'You dont have any pending tasks yei!') # respond with the builded list
      
    elif msg_text == '/remove':
      print('This should remove a todo from the TODO list')

    # we have to return the 200 response code so that telegram gets that we have received its msg
    return Response('ok', status=200)

  else:
    return '<h1> Esperanzo todo Bot </h1>'
