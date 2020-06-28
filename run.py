import dotenv
import os
import requests

from esperanzo_bot import app

if __name__ == '__main__':
  hostname = os.uname()[1]  
  if hostname == 'flask-server':
    # deploy
    print('should run gce deployment')
    app.run()
  else:
    # debug
    # if we run the script via the command line it will enter debug mode automatically
    print('Running in debug mode')
    app.run(debug=True)
  