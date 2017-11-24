from flask_wtf import Form
from wtforms import StringField, BooleanField, FloatField, IntegerField, DateField,TextAreaField, SelectField, FileField,validators
from wtforms.validators import DataRequired
from app.model import Upload
from datetime import datetime

class UploadExtratoForm(Form):
	 descricao = StringField('Descricao', validators=[DataRequired()])


class UploadDocForm(Form):
     extrato =  FileField('extrato')

class UploadRealizadoForm:
	descricao = StringField('Descricao', validators=[DataRequired()])

class ExtratoInfo():
	def __init__(self, data, desc, valor):
		self.data = data
		self.desc = desc
		self.valor = valor
