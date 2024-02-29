from flask import Flask, abort, render_template, redirect, url_for, flash
from forms import RegisterForm, LoginForm, AddTask, EditTask
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks-collection.db"
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)


class Tasks(db.Model):
    __tablename__ = "tasks_table"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users_table.id"))
    user_p = db.relationship("User", back_populates="tasks_c")
    task = db.Column(db.String(250), unique=False, nullable=False)
    completed = db.Column(db.Boolean)

class User(UserMixin, db.Model):
    __tablename__ = "users_table"
    id = db.Column(db.Integer, primary_key=True)
    tasks_c = db.relationship("Tasks", back_populates="user_p")
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/",  methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Please check your login details and try again.", 'error')
            return redirect(url_for("home"))

        login_user(user)
        return render_template("tasks.html")
    return render_template("index.html", form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        user = User()
        user.email = form.email.data
        user.name = form.name.data
        user.password = generate_password_hash(password=form.password.data, method="pbkdf2:sha256", salt_length=8)
        old_user = User.query.filter_by(email=user.email).first()
        if old_user:
            flash(f"This email already exists. Please log in instead.")
            return redirect(url_for("home"))
        else:

            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return render_template("tasks.html")
   
    return render_template("register.html", form=form, current_user=current_user)

@app.route("/add-task", methods=['GET', 'POST'])
def add_task():  
    form = AddTask()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            new_task = Tasks (
                task = form.task.data,
                completed = False,
                user_id = current_user.id
            )
            
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('tasks'))
    return render_template("add.html", form=form, current_user=current_user)
    

@app.route("/tasks")
def tasks():
    all_tasks = db.session.query(Tasks).all()
    uncompleted_task = Tasks.query.filter_by(completed=False, user_id=current_user.id).all()
    return render_template("tasks.html", tasks=all_tasks, uncompleted_task=uncompleted_task, current_user=current_user)


@app.route("/edit-task/<int:task_id>", methods=['GET', 'POST'])
def edit(task_id):
    new_task = db.get_or_404(Tasks, task_id)
    edit_form = EditTask(
        task=new_task.task,
        completed = False
    )
    if edit_form.validate_on_submit():
        new_task.task = edit_form.task.data
        db.session.commit()
        return redirect(url_for("tasks", task_id=new_task.id))
    return render_template("edit.html", form=edit_form, task=new_task, current_user=current_user)


@app.route("/check-task/<int:task_id>", methods=['GET', 'POST'])
def check_task(task_id): 
    completed_task = db.get_or_404(Tasks, task_id)
    completed_task.completed = True
    db.session.commit()
    return redirect(url_for("tasks"))

@app.route("/delete-task/<int:task_id>", methods=['GET', 'POST'])
def delete_task(task_id):
    task_to_delete = db.get_or_404(Tasks, task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for("tasks"))

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
