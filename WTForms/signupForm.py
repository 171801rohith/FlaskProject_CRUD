from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, InputRequired

class SignupForm(FlaskForm):
    name = StringField("NAME : ", validators=[DataRequired()])
    emailID = EmailField("EMAIL ID : ", validators=[DataRequired(), Email()])
    password = PasswordField("PASSWORD : ", validators=[InputRequired()])
    submit = SubmitField("SUBMIT")