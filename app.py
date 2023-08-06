from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(500), default="No Description")
    status = db.Column(db.Integer, default=0)

    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"


@app.route('/', methods = ['GET', 'POST']) #Index route
def index():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodos = Todo.query.all()
    return render_template('index.html', allTodos=allTodos)


@app.route('/update/<int:sno>', methods = ['GET', 'POST'])
def update(sno):
    if request.method == "POST":
        todo = Todo.query.filter_by(sno=sno).first()
        title = request.form['title']
        desc = request.form['desc']
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


@app.route('/change-status/<int:sno>')
def change_status(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if todo.status == 0:
        todo.status = 1
    else:
        todo.status = 0
    db.session.add(todo)
    db.session.commit()

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=3000)