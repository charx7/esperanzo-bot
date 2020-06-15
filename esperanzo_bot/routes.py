import json
import requests
import os
import dotenv

from esperanzo_bot import app # custom package import
from esperanzo_bot import db
from esperanzo_bot.models import Users, Todos
from esperanzo_bot.bot import TelegramBot

from flask import Flask
from flask import request
from flask import Response
from flask_sqlalchemy import SQLAlchemy


# Get env variables TODO should be separated
dotenv.load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
NGROK_URL = os.getenv('NGROK_URL')      
TelegramBot.webhook(BOT_TOKEN, NGROK_URL)
bot = TelegramBot(BOT_TOKEN)

@app.route("/", methods = ['POST', 'GET'])
def index():
  if request.method == 'POST':
    msg = request.get_json()
    bot.write_json(msg, 'telegram_request.json')

    # set the type of the msg
    try:
      msg['callback_query']
      bot.msg_type = 'callback'
      bot.chat_id = msg['callback_query']['message']['chat']['id'] # get the chat id to respond
      bot.msg_from = msg['callback_query']['from']['id'] # get the id of the person that sent the msg
      bot.msg_text = msg['callback_query']['data']
      bot.first_name = msg['callback_query']['message']['from']['first_name']
      bot.user_name = msg['callback_query']['message']['from']['username']
      
    except KeyError:
      bot.msg_type = 'user_text'
      bot.chat_id = msg['message']['chat']['id'] # get the chat id to respond
      bot.msg_from = msg['message']['from']['id'] # get the id of the person that sent the msg
      bot.msg_text = msg['message']['text']
      bot.first_name = msg['message']['from']['first_name']
      bot.user_name = msg['message']['from']['username']
    
    ### /greet command logic
    if bot.msg_text == '/greet':
      bot.send_message('Hey Patrona! 👋')

    ### /add command logic
    elif bot.msg_text[:4] == '/add':
      todo_text = bot.msg_text[4:].strip()
      found_user = Users.query.filter_by(id = bot.msg_from).first()
      
      if found_user:
        todo_to_add = Todos(todo_text=todo_text, owner_id=bot.msg_from)  
        db.session.add(todo_to_add)
        db.session.commit()
        bot.send_message('Added your new task.')
      else:
        print('Registering new user')
        # if we dont find any user we register it
        new_usr = Users(id = msg_from, first_name = bot.first_name, last_name= bot.last_name)
        db.session.add(new_usr)
        db.session.commit() # TODO there is no way of knowing if the insert was succesful :/?

        # add the todo 
        todo_to_add = Todos(todo_text=todo_text, owner_id=bot.msg_from)  
        db.session.add(todo_to_add)
        db.session.commit()
        bot.send_message('Added your new task.')
    
    #### /remind command
    elif bot.msg_text == '/remind':
      # case1 they are not registered
      # case2 they dont have any todos
      # case3 return a list of all the todos
      found_user = Users.query.filter_by(id = bot.msg_from).first()
      if found_user:
        # query all the todos of the user
        if len(found_user.todos) > 0:
          bot_response = 'Your pending tasks are: '
          for todo in found_user.todos:
            curr_text = todo.todo_text
            bot_response = bot_response + '\n -' + curr_text
          bot.send_message(bot_response) # respond with the builded list
        else:
          bot.send_message('You dont have any pending tasks yei!') # respond with the builded list
      
    # output Remove list bot command
    elif bot.msg_text == '/remove':
      # get the todo list
      found_user = Users.query.filter_by(id = bot.msg_from).first()
      if found_user:  
        todo_list = []
        if len(found_user.todos) > 0:
            for todo in found_user.todos:
              todo_list.append(todo.todo_text) 
        print('sending list: ', todo_list)
        res = bot.send_custom_keyboard('Please select one of the tasks to delete:', todo_list)
      else:
        bot.send_message('You dont have any pending tasks yei!')
    
    # remove a specific task
    elif bot.msg_text[:7] == '/delete':
      found_user = Users.query.filter_by(id = bot.msg_from).first()
      if found_user:  
        print('should delete a specific todo')
      else:
        bot.send_message('You dont have any pending tasks yeah!')
      
  #     callback_query_id = msg['callback_query']['id'] 
  #     msg_from = msg['callback_query']['message']['from']['id']
  #     callback_data = msg['callback_query']['data']
     
    return Response('ok', status=200)

  # if request.method == 'POST':
  #   msg = request.get_json() # the msg obj will be a json sent by telegram
  #   write_json(msg, 'telegram_request.json')

  #   # TODO this is a weird logic should change it
  #   try:
  #     msg['callback_query']
  #     msg_type = 'callback'
  #   except KeyError:
  #     msg_type = 'user_text'
    
  #   if msg_type == 'user_text':
  #     chat_id = msg['message']['chat']['id'] # get the chat id to respond
  #     msg_from = msg['message']['from']['id'] # get the id of the person that sent the msg
  #   else:
  #     callback_query_id = msg['callback_query']['id'] 
  #     msg_from = msg['callback_query']['message']['from']['id']
  #     callback_data = msg['callback_query']['data']


      
    
  #   # TODO the logic of parsing callback and simple commands should be separated
  #   elif msg_type == 'callback':
      
  #     # send the answer to the delete callback query
  #     res = send_callback_response(callback_query_id)
  #     write_json(res.json(), 'telegram_request.json') # TODO need to define what to do with the json

  #   # we have to return the 200 response code so that telegram gets that we have received its msg
  #   return Response('ok', status=200)

  # else:
  #   return '<h1> Esperanzo todo Bot </h1>'
