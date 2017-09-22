from flask_wtf import Form
from wtforms import StringField, BooleanField, FloatField, IntegerField, DateField,TextAreaField, SelectField, FileField, PasswordField,validators
from wtforms.validators import DataRequired, EqualTo
from app.model import Empresa

class UserForm(Form):
     nome       = StringField('Nome', validators=[DataRequired()])
     sobrenome  = StringField('SobreNome', validators=[DataRequired()])
     email      = StringField('E-Mail', validators=[DataRequired()])
     login      = StringField('Login', validators=[DataRequired()])
     password   = StringField('Password', validators=[DataRequired()])
     password   = PasswordField('New Password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
     confirm    = PasswordField('Repeat Password')
     empresa_id = SelectField('Empresa', coerce=int)

