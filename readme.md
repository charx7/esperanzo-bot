# Cloud deployment
## Create a self-signed certificate
In order to connect to telegram via a webhook we are going to need to establish an ssl connection, we will use a self-signed certificate. Ref https://stackoverflow.com/questions/45251809/telegram-getwebhookinfo-returns-ssl-error-ssl-routinestls-process-server-cert?noredirect=1&lq=1
```
  sudo openssl req -newkey rsa:2048 -sha256 -nodes -keyout PRIVATE.key -x509 -days 365 -out PUBLIC.pem -subj "/C=US/ST=New York/L=Brooklyn/O=Example Brooklyn Company/CN=<GCE_EXTERNAL_IP>"
```
Afterwards we need to setup nginx for the reverse proxy configuration:
```
  vim /etc/nginx/sites-available/esperanzo
  ...
  server {
  listen 80;
  listen 443 ssl;
  server_name <GCE_EXTERNAL_IP>;
  ssl_certificate /home/PUBLIC.pem;
  ssl_certificate_key /home/PRIVATE.key;

  location /<BOT_TOKEN> {
    proxy_set_header Host $http_host;
    proxy_redirect off;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Scheme $scheme;
    proxy_pass http://0.0.0.0:5000/;
    }
  }
  ...
```

## Manually set the webhook
`curl -F "url=https://<GCE_EXTERNAL_IP>/<BOT_TOKEN>" -F "certificate=@/home/PUBLIC.pem" https://api.telegram.org/bot<BOT_TOKEN>/setWebhook`

## Debug webhook
`https://api.telegram.org/bot<BOT_TOKEN>/getWebhookinfo`

## Set-up hostname to deploy to production 
`sudo hostnamectl set-hostname flask-server`
## Change the hostname
vim /etc/hosts
```
  ...
  CLOUD_VM_IP flask-server
  ...
```
## Create a venv
Install python3-venv `sudo apt install python3-venv` create a virtual environment for the bot `python3 -m venv python-virtual-envs/bot-env`

# Flask commands
To run flask on an specific port 
```
  export FLASK_APP=run.py
  flask run --host=0.0.0.0
```
To run it with `gunicorn` while on the venv and with gunicorn installed:
```
  #gunicorn -w <number of workers> <Name of the script>:<name of the flask app>
  gunicorn -w 1 run:app
```
To run in debug mode just execute the `run.py` script while on the virtual environment

# Ngrok commands
`./ngrok http 5000`

# Basic flask-sqlalchemy commands
```
  u1 = app.Users(id = 1, first_name = 'test', last_name= 'test2')
  db.session.add(u1)
  db.session.commit()
  r = Users.query.all()
  print(r)

  todo1 = Todos(todo_text='tienes que..', owner_id=1)
  db.session.add(todo1)
  db.session.commit()
  
```

# Esperanzo TODO LIST
1. Refactor and separate the flask and command logic
2. add nlp intent instead of raw commands
3. fix webhook logic
4. remove the /register command
