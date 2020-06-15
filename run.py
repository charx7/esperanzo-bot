import dotenv
import os
import requests

from esperanzo_bot import app

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

# Get env variables TODO should be separated
dotenv.load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
NGROK_URL = os.getenv('NGROK_URL')      

# do the webhook
r = webhook()

if __name__ == '__main__':
  # if we run the script via the command line it will enter debug mode automatically
  app.run(debug=True)
  
