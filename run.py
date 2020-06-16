import dotenv
import os
import requests

from esperanzo_bot import app

if __name__ == '__main__':
  # if we run the script via the command line it will enter debug mode automatically
  app.run(debug=True)
  