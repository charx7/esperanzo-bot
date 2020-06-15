# Ngrok commands
./ngrok http 5000

# Basic flask-sqlalchemy commands
```
  u1 = app.Users(id = 1, first_name = 'test', last_name= 'test2')
  app.db.session.add(u1)
  app.db.session.commit()
  r = app.Users.query.all()
  print(r)

  todo1 = app.Todos(todo_text='tienes que..', owner_id=1)
  app.db.session.add(todo1)
  app.db.session.commit()
  
```

# Esperanzo TODO LIST
1. Refactor and separate the flask and command logic
2. add nlp intent instead of raw commands
3. fix webhook logic
4. remove the /register command
