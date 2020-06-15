from esperanzo_bot import db

class Users(db.Model):
  '''
    This class defines the users table in which we are going
    to save the owners of the todos
  '''
  __tablename__ = "Users"

  id = db.Column('id', db.Integer, primary_key = True)
  first_name = db.Column('first_name', db.String(100))
  last_name = db.Column('last_name', db.String(100))
  todos = db.relationship('Todos', backref='author', lazy=True)

  def __init__(self, id, first_name, last_name):
    self.id = id
    self.first_name = first_name
    self.last_name = last_name 

  def __str__(self):
    '''
      What will be displayed if a User is called from the print() method
    '''
    return f'<User id: {self.id}, first_name: {self.first_name}, last_name: {self.last_name}>'

class Todos(db.Model):
  '''
    Defines the TODOS table, we are going to save all of our todos here.
  '''
  __tablename__ = "TODOS"

  id = db.Column(db.Integer, primary_key=True)
  todo_text = db.Column(db.String, nullable=False)
  owner_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable = False)
  #owner_name_relationship = db.relationship('Users', foreign_keys='Todos.owner_id')

  def __init__(self, todo_text, owner_id):
    self.todo_text = todo_text
    self.owner_id = owner_id

  def __str__(self):
    return f'<TODO id: {self.id}, todo: {self.todo_text}, owner_id: {self.owner_id}'
