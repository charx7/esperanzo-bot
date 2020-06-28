# Cloud deployment
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
