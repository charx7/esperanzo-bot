import requests
import json

class TelegramBot:
  def __init__(self, BOT_TOKEN):
    self.chat_id = None
    self.msg_from = None
    self.first_name = None
    self.msg_type = None
    self.msg_text = None
    self._BOT_TOKEN = BOT_TOKEN
    self._NGROK_URL = None
    self.msg_id = None # maybe not in use
    self.update_id = None
    self.callback_query_id = None

  def send_callback_response(self):
    '''
      Sends a response to a callback query from the telegram API
    '''
    url = f'https://api.telegram.org/bot{self._BOT_TOKEN}/answerCallbackQuery'
    # define a json object to send via requests
    print('here')
    json = {
      'callback_query_id': self.callback_query_id,
      'text': 'Deleted task 🧹'
    }

    return requests.post(url, json=json)

  def send_custom_keyboard(self, msg, reply_list):
    '''
      Sends back a custom keyboard with different options
      
      Args:
        chat_id (str): chat_id to send
        msg (str): msg to send
        reply_list (list<str>): list of todo elemenents that will appear in the 
        custom keyboard
    '''
    # construct the keyboard options
    keyboard_ops = [[{'text': todo.todo_text, 'callback_data': '/delete ' + str(todo.id)}] for todo in reply_list]

    keyboard_replies =  {'inline_keyboard': keyboard_ops,
      # [[{'text': 'holi', 'callback_data': 'dummy'}],
      # [{'text': 'holi2', 'callback_data': 'dummy'}]]
      'resize_keyboard': True}
  
    url = f'https://api.telegram.org/bot{self._BOT_TOKEN}/sendMessage'
 
    json = {
      'chat_id': self.chat_id,
      'text': msg,
      'reply_markup': keyboard_replies
    }

    r = requests.post(url, json=json)
    return r

  def edit_reply_markup(self, new_reply_list):
    # construct the keyboard options
    keyboard_ops = [[{'text': todo.todo_text, 'callback_data': '/delete ' + str(todo.id)}] for todo in new_reply_list]

    # Dummy data to debug
    # keyboard_ops =  {'inline_keyboard': [
    #   [{'text': 'holi', 'callback_data': 'dummy'}],
    #   [{'text': 'holi2', 'callback_data': 'dummy'}]
    #   ],
    #   'resize_keyboard': True}
    
    url = f'https://api.telegram.org/bot{self._BOT_TOKEN}/editMessageReplyMarkup'
    # define a json object to send via requests
    json = {
      'chat_id': self.chat_id,
      'message_id': self.msg_id,
      'reply_markup': {
        'inline_keyboard': keyboard_ops,
        'resize_keyboard': True
      }
    }

    r = requests.post(url, json=json)
    return r

  def send_message(self, msg):
    '''
      Will send a message to the current given chat-id

      Args:
        chat_id (str): chat id in string format
        msg (str): message to send
      
      Returns:
        (tbd)
    '''
    url = f'https://api.telegram.org/bot{self._BOT_TOKEN}/sendMessage'
    # define a json object to send via requests
    json = {
      'chat_id': self.chat_id,
      'text': msg
    }
    r = requests.post(url, json=json)
    return r

  @staticmethod
  def write_json(data, filename='response.json'):
    '''
      This function will write a json object into the directory

      Args:
        data (json): json object
    '''
    with open('./esperanzo_bot/' + filename, 'w') as f:
      json.dump(data, f, indent=4, ensure_ascii=False)


  @staticmethod
  def webhook(BOT_TOKEN, HOOK_URL, hostname):
    '''
      Method sets the webhook -> should be another thing
    '''
    print('Setting the webhook for telegram')
    if hostname == 'flask-server':
      # set the webhook for deployment
      url = f'https://api.telegram.org/bot{BOT_TOKEN}/setWebHook?url={HOOK_URL}'
      cert_path = '/home/PUBLIC.pem'
      key_path = '/home/PRIVATE.pem'
      cert = (cert_path, key_path)
      print('the paths are: ',cert_path, ' ',key_path)
      res = requests.get(url, cert=cert)

    else:
      url = f'https://api.telegram.org/bot{BOT_TOKEN}/setWebHook?url={HOOK_URL}'
      print(url)
      res = requests.get(url)
    
    json_res = res.json()
    print(json_res['description'])

    return json_res
