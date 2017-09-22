from flask_wtf import Form
from wtforms import StringField, BooleanField, FloatField, IntegerField, DateField,TextAreaField, SelectField, FileField, PasswordField,validators
from wtforms.validators import DataRequired, EqualTo
from app.model import Empresa

class LoginForm(Form):
     login       = StringField('login', validators=[DataRequired()])
     password    = PasswordField('Password',validators=[DataRequired()])

