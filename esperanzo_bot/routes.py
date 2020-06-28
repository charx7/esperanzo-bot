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
HOOK_URL = os.getenv('HOOK_URL') 
hostname = os.uname()[1] # hostname to differentiate between prod and dev
TelegramBot.webhook(BOT_TOKEN, HOOK_URL, hostname)
bot = TelegramBot(BOT_TOKEN)

@app.route("/", methods = ['POST', 'GET'])
def index():
  if request.method == 'POST':
    msg = request.get_json()
    bot.write_json(msg, 'telegram_request.json')

    # set the type of the msg
    try:
      # TODO borrar last_name y username de las propiedades de la clase BOT 
      msg['callback_query']
      bot.msg_type = 'callback'
      bot.chat_id = msg['callback_query']['message']['chat']['id'] # get the chat id to respond
      bot.msg_from = msg['callback_query']['from']['id'] # get the id of the person that sent the msg
      bot.msg_text = msg['callback_query']['data']
      bot.first_name = msg['callback_query']['message']['from']['first_name']
      bot.callback_query_id = msg['callback_query']['id']
      bot.msg_id = msg['callback_query']['message']['message_id'] # msg id for editing the inline keyboard reply
      
    except KeyError:
      bot.msg_type = 'user_text'
      bot.chat_id = msg['message']['chat']['id'] # get the chat id to respond
      #bot.msg_id = msg['callback_query']['message']['message_id']
      bot.msg_from = msg['message']['from']['id'] # get the id of the person that sent the msg
      bot.msg_text = msg['message']['text']
      bot.first_name = msg['message']['from']['first_name']
      
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
        new_usr = Users(id = bot.msg_from, first_name = bot.first_name)
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
              todo_list.append(todo) 
        print('sending list: ', todo_list)
        res = bot.send_custom_keyboard('Please select one of the tasks to delete:', todo_list)
      else:
        bot.send_message('You dont have any pending tasks yei!')
    
    # remove a specific task
    elif bot.msg_text[:7] == '/delete':
      found_user = Users.query.filter_by(id = bot.msg_from).first()

      if found_user:  
        print('should delete a specific todo')
        id_to_del = int(bot.msg_text[7:].strip())
        r = Todos.query.filter_by(id = id_to_del).delete()
        db.session.commit()

        # query again to avoid double listing?
        found_user = Users.query.filter_by(id = bot.msg_from).first()
        new_todos = found_user.todos
        
        bot.edit_reply_markup(new_todos) # edit the reply text
        bot.send_callback_response() # to get the broom notification
      else:
        bot.send_message('You dont have any pending tasks yeah!')
      
    return Response('ok', status=200)
  else:
    return 'Esperanzo-BOT API'
    