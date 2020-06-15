import requests
import json

class TelegramBot:
  def __init__(self, BOT_TOKEN):
    self.chat_id = None
    self.msg_from = None
    self.first_name = None
    self.user_name = None
    self.msg_type = None
    self.msg_text = None
    self._BOT_TOKEN = BOT_TOKEN
    self._NGROK_URL = None
    self.callback_query_id = None

  def send_callback_response(self):
    '''
      Sends a response to a callback query from the telegram API
    '''
    url = f'https://api.telegram.org/bot{self._BOT_TOKEN}/answerCallbackQuery'
    # define a json object to send via requests
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
        reply_list (list<str>): list of elemenents that will appear in the 
        custom keyboard
    '''
    # construct the keyboard options
    keyboard_ops = [[{'text': todo, 'callback_data': '/delete ' + todo}] for todo in reply_list]

    print(keyboard_ops[0:2])
    #keyboard_replies =  { "inline_keyboard": [keyboard_ops]}
    keyboard_replies =  {'inline_keyboard': keyboard_ops,
      # [[{'text': 'holi', 'callback_data': 'dummy'}],
      # [{'text': 'holi2', 'callback_data': 'dummy'}]]
      'resize_keyboard': True}
  
    url = f'https://api.telegram.org/bot{self._BOT_TOKEN}/sendMessage'
    # define a json object to send via requests
    json = {
      'chat_id': self.chat_id,
      'text': msg,
      'reply_markup': keyboard_replies
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
  def webhook(BOT_TOKEN, NGROK_URL):
    '''
      Method sets the webhook -> should be another thing
    '''
    print('Setting the webhook for telegram')
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/setWebHook?url={NGROK_URL}'
    print(url)
    res = requests.get(url)
    json_res = res.json()
    
    print(json_res['description'])

    return json_res

