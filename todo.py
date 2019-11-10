from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/Ozgur/dev/Flask_ToDo/todo.db"
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)


@app.route("/")
def index():
    data = Todo.query.all()
    return render_template("index.html", todos=data)


@app.route("/add", methods=["POST"])
def addTodo():
    todoTitle = request.form.get(
        "title"
    )  # index.html' de name = "title" olan bilgiyi alma - JS
    newTodo = Todo(title=todoTitle, complete=False)
    db.session.add(newTodo)
    db.session.commit()

    return redirect(url_for("index"))


# todo tamamlama
@app.route("/complete/<string:id>")
def complete(id):
    todo = Todo.query.filter_by(id=id).first()
    # if todo.complete == True:
    #     todo.complete == False
    # else:
    #     todo.complete == True

    todo.complete = not todo.complete
    db.session.commit()

    return redirect(url_for("index"))


# todo silme
@app.route("/delete/<string:id>")
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("index"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

