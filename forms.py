from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()], render_kw={"class": "label login-form box"})
    email = StringField("Email", validators=[DataRequired()], render_kw={"class": "label login-form box"})
    password = StringField("Password", validators=[DataRequired()], render_kw={"class": "label login-form box"})
    submit = SubmitField("Register", render_kw={"class": "btn-form"})

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], render_kw={"class": "label login-form box"})
    password = StringField('Password', validators=[DataRequired()], render_kw={"class": "label login-form box"})
    submit = SubmitField("Login", render_kw={"class": "btn-form"})

class AddTask(FlaskForm):
    task = StringField("Add Task", validators=[DataRequired()], render_kw={"class": "label login-form box"})
    submit = SubmitField("Add +", render_kw={"class": "edit-task"})

class EditTask(FlaskForm):
    task = StringField("Edit Task", validators=[DataRequired()], render_kw={"class": "label login-form box"})
    submit = SubmitField("Edit", render_kw={"class": "edit-task"})

    