from flask import Flask, render_template, url_for, redirect, request
from forms import RegisterForm, LoginForm, AddTask
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

@app.route("/",  methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        return render_template("tasks.html")
    return render_template("index.html", form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return render_template("tasks.html")
   
    return render_template("register.html", form=form)

@app.route("/add-task", methods=['GET', 'POST'])
def add():
    form = AddTask()
    return render_template("add.html", form=form)
    

@app.route("/tasks")
def tasks():
    return render_template("tasks.html")

if __name__ == "__main__":
    app.run(debug=True)
