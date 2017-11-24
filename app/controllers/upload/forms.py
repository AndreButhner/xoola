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

class ExtratoInfo(object):
    def __init__(self, row):
        self.data = ''
        self.desc = ''
        self.valor = 0
        self.saldo = 0
        for i in range(0, 6):
            #print (row[i].value)
            if row[i].value != (None):
                if i == 0:
                    self.data = row[i].value
                    print(self.data)
                if i == 3:
                    self.desc = row[i].value
                    print(self.desc)
                if i == 4:
                    self.valor = row[i].value
                    print (self.valor)
                if i == 5:
                    self.saldo = row[i].value
                    print (self.saldo)


