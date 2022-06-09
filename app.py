#### PACKAGES ###
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


load_dotenv()

# UNAME = os.environ["UNAME"]
# PWD = os.environ["PWD"]
# DB = os.environ["DB"]
DATABASE_URL = os.environ["DATABASE_URL"]


app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{UNAME}:{PWD}@localhost/{DB}"
app.config['SQLALCHEMY_DATABASE_URI'] = f'{DATABASE_URL}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()

db.app = app
db.init_app(app)

app.secret_key = "ABC"




### DATABASE ###

class Todo(db.Model):
    __tabelname__ = "todo-db"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route('/')
def index():
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template('base.html', todo_list=todo_list)

@app.route('/add', methods=['POST','GET'])
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)