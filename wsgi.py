import click, sys
from models import db, User, Todo
from sqlalchemy.exc import IntegrityError
from app import app


@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.init_app(app)
    db.create_all()
    bob = User('bob', 'bob@mail.com', 'bobpass')
    bob.todos.append(Todo('wash car'))
    db.session.add(bob)
    db.session.commit()
    print(bob)
    print('database intialized')


@app.cli.command("get-user", help="Retrieves a User by username or id")
@click.argument('key', default='bob')
def get_user(key):
    bob = User.query.filter_by(username=key).first()
    if not bob:
      bob = User.query.get(int(key))
      if not bob:
        print(f'{key} not found!')
        return
    print(bob)


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


@app.cli.command('get-users')
def get_users():
    users = User.query.all()
    print(users)


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
      db.session.rollback()
      print(e.orig)
      print("Username or email already taken!")
    else:
      print(newuser)


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


@app.cli.command('add-todo')
@click.argument('username', default='bob')
@click.argument('text', default='wash car')
def add_task(username, text):
    bob = User.query.filter_by(username=username).first()
    if not bob:
      print(f'{username} not found!')
      return
    new_todo = Todo(text)
    bob.todos.append(new_todo)
    db.session.add(bob)
    db.session.commit()
    print('Todo added!')


@app.cli.command('get-todos')
@click.argument('username', default='bob')
def get_user_todos(username):
    bob = User.query.filter_by(username=username).first()
    if not bob:
      print(f'{username} not found!')
      return
    print(bob.todos)


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

@click.argument('category', default='chores')
@click.argument('username', default='bob')
@click.argument('todo_id', default=1)
@app.cli.command('add-category', help="Adds a category to a todo")
def add_todo_category_command(category, todo_id, username,):
    user = User.query.filter_by(username=username).first()
    if not user:
      print(f'user {username} not found!')
      return

    res = user.add_todo_category(todo_id, category)
    if not res:
      print(f'{username} has no todo id {todo_id}')
      return

    todo = Todo.query.get(todo_id)
    print(todo)