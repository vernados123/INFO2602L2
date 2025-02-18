import click, sys
from models import db, User, Todo
from app import app
from sqlalchemy.exc import IntegrityError


@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.init_app(app)
  db.create_all()
  bob = User('bob', 'bob@mail.com', 'bobpass')
  #new_todo = bob.create_todo("wash car")
  print(bob)
  print('database intialized')
  db.session.add(bob)
  #db.session.add(new_todo)
  db.session.commit()
  print(bob)

@app.cli.command('delete-user')
@click.argument('username', default='bob')
def delete_user(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
      print(f'{username} not found!')
      return
  db.session.delete(bob)
  db.session.commit()
  print(f'{username} deleted')

@app.cli.command("get-user", help="Retrieves a User")
@click.argument('username', default='bob')
def get_user(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} not found!')
    return
  print(bob)

@app.cli.command('get-users')
def get_users():
  # gets all objects of a model
  users = User.query.all()
  print(users)

@app.cli.command("change-email")
@click.argument('username', default='bob')
@click.argument('email', default='bob@mail.com')
def change_email(username, email):
  bob = User.query.filter_by(username=username).first()
  if not bob:
      print(f'{username} not found!')
      return
  bob.email = email
  db.session.add(bob)
  db.session.commit()
  print(bob)

@app.cli.command('create-user')
@click.argument('username', default='rick')
@click.argument('email', default='rick@mail.com')
@click.argument('password', default='rickpass')
def create_user(username, email, password):
  newuser = User(username, email, password)
  try:
    db.session.add(newuser)
    db.session.commit()
  except IntegrityError as e:
    #let's the database undo any previous steps of a transaction
    db.session.rollback()
    # print(e.orig) #optionally print the error raised by the database
    print("Username or email already taken!") #give the user a useful message
  else:
    print(newuser) # print the newly created user

#just putting this here for the lab but i cant firgure out why my code in models.py is unreachable after the new todos command

@app.cli.command('get-todos')
@click.argument('username', default='bob')
def get_user_todos(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
      print(f'{username} not found!')
      return
  print(bob.todos)

  @app.cli.command('add-todo')
  @click.argument('username', default='bob')
  @click.argument('text', default='Mow lawn')
  def add_task(username, text):
    bob = User.query.filter_by(username=username).first()
    if not bob:
        print(f'{username} not found!')
        return
    new_todo = Todo(text)
    bob.todos.append(new_todo)
    db.session.add(bob)
    db.session.commit()

@app.cli.command('get-todos')
def get_todos():
  todos = Todo.query.all()
  print(todos)

@click.argument('todo_id', default=1)
@click.argument('username', default='bob')
@app.cli.command('toggle-todo')
def toggle_todo_command(todo_id, username):
  user = User.query.filter_by(username=username).first()
  if not user:
    print(f'{username} not found!')
    return

  todo = Todo.query.filter_by(id=todo_id, user_id=user.id).first()
  if not todo:
    print(f'{username} has no todo id {todo_id}')

  todo.toggle()
  print(f'{todo.text} is {"done" if todo.done else "not done"}!')
