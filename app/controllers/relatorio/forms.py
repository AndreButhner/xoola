from flask_wtf import Form
from wtforms import StringField, BooleanField, FloatField, IntegerField, DateField,TextAreaField, SelectField, FileField,validators
from wtforms.validators import DataRequired
from app.model import Categoria,Formapagamento, Movimentacao
from datetime import datetime

class PesForm(Form):     
     categoria_id = SelectField('categorias')
     conta_id     = SelectField('Conta')
     data         = StringField('Data')
     